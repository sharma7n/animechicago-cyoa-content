FROM gitpod/workspace-postgres

# Configure Django for gitpod development
ENV DJANGO_SECRET_KEY="gitpod"
ENV DJANGO_DB_NAME="postgres"
ENV DJANGO_DB_USERID="gitpod"
ENV DJANGO_DB_PASSWORD="gitpod"
ENV DJANGO_SUPERUSER_PASSWORD="An1m3#Ch1c4g0"
ENV DJANGO_GITPOD=true

