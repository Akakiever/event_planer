FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=event_planer.settings
WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt
COPY /src/ /src/