from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.filters import EventDateFilter
from core.models import Event
from core.serializers import EventSerializer, UserLoginSerializer, UserRegistrationSerializer
from core.tasks import send_event_email_register
from permitions import OnlyOrganizerEdit


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(username=serializer.data['username']).first()
            if user and user.check_password(serializer.data['password']):
                token, _ = Token.objects.get_or_create(user=user)
                response_data = {
                    'token': token.key
                }
                return Response(response_data, status=status.HTTP_200_OK)
            response_data = {
                "non_field_errors": ["User does not exist"]
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            response = {
                'token': token.key
            }
            return Response(response, status=status.HTTP_201_CREATED)
        raise ValidationError(
            serializer.errors, code=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, OnlyOrganizerEdit]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = EventDateFilter
    search_fields = ['title', 'description', 'location']

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()

        if event.organizer == request.user:
            return Response({'message': 'You can not register to your own event'}, status=status.HTTP_403_FORBIDDEN)

        if event.attendees.filter(id=request.user.id).exists():
            return Response({'message': 'You are already registered'}, status=status.HTTP_400_BAD_REQUEST)

        event.attendees.add(request.user)
        send_event_email_register.apply_async((event.id, request.user.id))
        return Response(status=status.HTTP_204_NO_CONTENT)
