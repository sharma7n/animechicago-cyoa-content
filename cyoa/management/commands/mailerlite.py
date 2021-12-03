import os

from django.core.management.base import BaseCommand, CommandError
from cyoa.api import SendMailRequest
from cyoa.mail import add_subscriber, count_subscribers

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--add',
            type=str,
            nargs=1,
            help='email address to add to subscribers',
        )
    
    def handle(self, *args, **options):
        add = options.get('add', '')
        if add:
            r = add_subscriber(add[0])
            print(r)