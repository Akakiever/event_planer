from rest_framework import permissions


class OnlyOrganizerEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not (request.method in ("PUT", "PATCH") and obj.organizer != request.user)
