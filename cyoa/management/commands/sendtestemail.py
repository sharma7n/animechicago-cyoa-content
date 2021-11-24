from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

class Command(BaseCommand):
    def handle(self, *args, **options):
        send_mail(
            "test",
            "test",
            "atom-noreply@bot.animechicago.com",
            ["sharma7n@gmail.com"],
        )