FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8001"]
#CMD ["sh", "-c", "python manage.py migrate && python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(username='admin', password='1')\" && python manage.py runserver 0.0.0.0:8001"]
