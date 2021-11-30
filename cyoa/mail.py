import attr
import requests

from django.template.loader import render_to_string

from config.settings import MAILGUN_API_KEY, MAILGUN_DOMAIN
from cyoa.api import SendMailRequest

API_ROOT = f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}'
AUTH = ('api', MAILGUN_API_KEY)
FROM = f'AnimeChicago Advice Bot <noreply@{MAILGUN_DOMAIN}>'
SUBJECT = "Your Anime Recommendation!"

def send_mail(smr: SendMailRequest):
    html = render_to_string('email.html', context=attr.asdict(smr))
    data = {
        'from': FROM,
        'to': [smr.to],
        'subject': SUBJECT,
        'html': html,
    }

    return requests.post(
        f'{API_ROOT}/messages',
        auth=AUTH,
        data=data,
    )