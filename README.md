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

### Set up email API credentials

You will need to set the environment variables `MAILERLITE_API_KEY`, `MAILGUN_API_KEY`, and `MAILGUN_DOMAIN` manually (even if using gitpod). Contact one of the AnimeChicago staff for these values. The development server will still run without these, but none of the email functionality (including the /mail route) will work correctly.

### Launch the Development Server

`pipenv run python manage.py runserver`

## Deployment

The content server is hosted on Heroku. All commits to the master branch will automatically trigger new deployments in Heroku, and the new version of the app will start running as soon as the deployment finishes (which usually takes less than a minute).

If you need to change something on Heroku directly (which includes, but is not limited to, changing credentials for third-party services used in production, such as Mailerlite and Mailgun credentials), please contact sharma7n@gmail.com
