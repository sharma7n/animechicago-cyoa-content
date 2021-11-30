import os

from django.core.management.base import BaseCommand, CommandError
import requests

from config.settings import FROM_EMAIL

class Command(BaseCommand):
    def handle(self, *args, **options):
        MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', '')
        if not MAILGUN_API_KEY:
            raise CommandError("missing env MAILGUN_API_KEY")
        
        MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', '')
        if not MAILGUN_DOMAIN:
            raise CommandError("missing env MAILGUN_DOMAIN")
        
        API_ROOT = f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}'

        auth = ('api', MAILGUN_API_KEY)
        data = {
            'from': f"AnimeChicago Advice Bot <noreply@{MAILGUN_DOMAIN}>",
            'to': ["sharma7n@gmail.com"],
            'subject': "sendtestemail",
            'text': "sendtestemail",
        }
        
        r = requests.post(
		    f'{API_ROOT}/messages',
            auth=auth,
            data=data,
        )
        
        print(r)