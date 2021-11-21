FROM gitpod/workspace-postgres

# Configure Django for gitpod development
ENV DJANGO_SECRET_KEY="gitpod"
ENV DJANGO_DB_NAME="localhost"
ENV DJANGO_DB_USERID="gitpod"
ENV DJANGO_DB_PASSWORD="gitpod"
ENV DJANGO_SUPERUSER_PASSWORD="gitpod"
ENV DJANGO_GITPOD=true