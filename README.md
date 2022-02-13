# Environments

Create file `.env`

Provide in file this values:

```
DJANGO_SECRET_KEY=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=
DB_HOST=        # For use local database, set `host.docker.internal`     
```

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Create awards

```bash
docker-compose run --rm web python manage.py createawards
```

* Pictures for awards added in admin panel!

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

Create superuser

```bash
docker-compose run --rm web python manage.py createsuperuser
```
