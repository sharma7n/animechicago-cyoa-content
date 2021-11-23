# AnimeChicago CYOA Content Manager

Content manager for the AnimeChicago CYOA application.

## Functionality

Log in as an administrator user, and create, update, or delete questions.

## Development

### Initial Setup

Recommended: Create a new [gitpod](https://gitpod.io) workspace from this repository. All of the required setup will be performed and the server will be started automatically.

If you're not using gitpod, or you need to set things up manually, please follow these instructions:

1. Configure a [PostgreSQL](https://www.postgresql.org/) database.
1. Set the following environment variables: `DJANGO_SECRET_KEY`, `DJANGO_DB_NAME`, `DJANGO_DB_USERID`, `DJANGO_DB_PASSWORD`, `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`.
1. Run `bash app-bootstrap-dev.sh`.

### Launch the Development Server

`pipenv run python manage.py runserver`