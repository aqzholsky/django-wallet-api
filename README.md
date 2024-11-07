### Quickstart

#### Generate secret key
```sh
python -c 'import secrets; print("".join(secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)))'
```

#### Create ``.env`` file (or rename and modify ``.env.example``) in project root and set environment variables for application: ::
```shell
touch .env
echo "DEBUG=True" >> .env
echo "MYSQL_ROOT_PASSWORD=root_password" >> .env
echo "MYSQL_DATABASE=database_name" >> .env
echo "MYSQL_USER=database_user" >> .env
echo "MYSQL_PASSWORD=database_password" >> .env
echo "MYSQL_PORT=3306" >> .env
echo "DJANGO_ADMIN_USERNAME=admin" >> .env
echo "DJANGO_ADMIN_EMAIL=admin@gmail.com" >> .env
echo "DJANGO_ADMIN_PASSWORD=admin" >> .env
```

#### Run docker container
```bash
docker-compose up -d --build
```

### Swagger Documentation
You can access the automatically generated Swagger documentation for the API at http://localhost:8000/swagger
