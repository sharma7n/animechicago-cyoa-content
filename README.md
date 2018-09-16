# AnimeChicago CYOA Content Manager

Content manager for the AnimeChicago CYOA application.

## Functionality

Log in as an administrator user, and create, update, or delete questions.

## Development

### Initial Setup

The following steps assume a fresh Cloud9 workspace.

1. Run: `bash app-bootstrap.sh`
2. Configure postgres locally: https://community.c9.io/t/setting-up-postgresql/1573
3. Create an admin user: `pipenv run python manage.py createsuperuser`

### Launch the Development Server

`pipenv run python manage.py runserver $IP:$PORT`