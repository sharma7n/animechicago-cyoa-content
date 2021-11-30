import os

from django.core.management.base import BaseCommand, CommandError
from cyoa.api import SendMailRequest
from cyoa.mail import send_mail

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'to',
            type=str,
            nargs=1,
            help='address to send test email to',
        )
        parser.add_argument(
            '-r',
            '--recommendation',
            type=str,
            nargs=1,
            help='recommendation',
        )
        parser.add_argument(
            '-s',
            '--source',
            type=str,
            nargs=1,
            help='source',
        )
    
    def handle(self, *args, **options):
        to = options['to']
        recommendation = options.get('recommendation', "One Piece")
        source = options.get('source', "Netflix")

        req = SendMailRequest(
            to=to,
            recommendation=recommendation[0],
            source=source[0],
        )

        r = send_mail(req)
        print(r, r.text)