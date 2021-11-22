import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates the admin user in a dev environment'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        if not username:
            raise CommandError('DJANGO_SUPERUSER_USERNAME must be nonempty')
        
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        if not password:
            raise CommandError('DJANGO_SUPERUSER_PASSWORD must be nonempty')
        
        User.objects.create_superuser(username, 'a@none.com', password)