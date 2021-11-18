FROM gitpod/workspace-postgres

# Configure Django for gitpod development
ENV DJANGO_SECRET_KEY="gitpod"
ENV DJANGO_DB_NAME="gitpod-db"
ENV DJANGO_DB_USERID="gitpod"
ENV DJANGO_DB_PASSWORD="gitpod"