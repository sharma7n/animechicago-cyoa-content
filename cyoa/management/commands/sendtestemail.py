from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

from settings import FROM_EMAIL

class Command(BaseCommand):
    def handle(self, *args, **options):
        send_mail(
            "test",
            "test",
            FROM_EMAIL,
            ["sharma7n@gmail.com"],
        )