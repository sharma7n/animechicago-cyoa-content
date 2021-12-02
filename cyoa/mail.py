import attr
import requests

from django.template.loader import render_to_string
from mailerlite import MailerLiteApi

from config.settings import MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILERLITE_API_KEY
from cyoa.api import SendMailRequest

MAILERLITE_SUBSCRIBERS_GROUP = 109448996

MAIGUN_API_ROOT = f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}'
MAILGUN_AUTH = ('api', MAILGUN_API_KEY)

FROM = f'AnimeChicago\'s Advice Bot <bot@{MAILGUN_DOMAIN}>'
SUBJECT = "🤖 Your Next Anime Obsession Is..."

def send_mail(smr: SendMailRequest):
    html = render_to_string('email.html', context=attr.asdict(smr))
    print(html)
    data = {
        'from': FROM,
        'to': [smr.to],
        'subject': SUBJECT,
        'html': html,
    }

    if smr.subscribe:
        add_subscriber(smr.to)
    
    return requests.post(
        f'{MAIGUN_API_ROOT}/messages',
        auth=MAILGUN_AUTH,
        data=data,
    )

def add_subscriber(subscriber: str):
    subscribers_data = {
        'name': "", # MailerLite API requires name for subscribers data but we don't want to collect that in the UI.
        'email': subscriber,
    }
    return MailerLiteApi(MAILERLITE_API_KEY).groups.add_single_subscriber(MAILERLITE_SUBSCRIBERS_GROUP, subscribers_data)

def list_subscribers():
    return MailerLiteApi(MAILERLITE_API_KEY).groups.subscribers(MAILERLITE_SUBSCRIBERS_GROUP)