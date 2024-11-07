#!/bin/bash

python manage.py migrate && python manage.py collectstatic --noinput

echo "from django.contrib.auth import get_user_model;User = get_user_model(); \
User.objects.create_superuser('${DJANGO_ADMIN_USERNAME}', '${DJANGO_ADMIN_EMAIL}', '${DJANGO_ADMIN_PASSWORD}')" \
  | python manage.py shell

exec "$@"
