import requests

from config.settings import MAILGUN_API_KEY, MAILGUN_DOMAIN
from cyoa.api import SendMailRequest

API_ROOT = f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}'
AUTH = ('api', MAILGUN_API_KEY)
FROM = f'AnimeChicago Advice Bot <noreply@{MAILGUN_DOMAIN}>'
SUBJECT = "Your Anime Recommendation!"

def send_mail(req: SendMailRequest):
    data = {
        'from': FROM,
        'to': [req.to],
        'subject': SUBJECT,
        'text': f"You should watch {req.recommendation}! It's streaming on {req.source}."
    }

    return requests.post(
        f'{API_ROOT}/messages',
        auth=AUTH,
        data=data,
    )