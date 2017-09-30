import json
import requests

import argparse
from django.core.management.base import BaseCommand
from optparse import make_option

from bots.settings.base import MESSENGER


class Command(BaseCommand):

    help = 'Set up Messenger get_started button'

    def add_arguments(self, parser):
        parser.add_argument('GET_STARTED_PAYLOAD', action='store', help='User defined get_started button payload', type=str),

    def handle(self, *args, **options):
        print(self._send_properties(options['GET_STARTED_PAYLOAD']))

    def _send_properties(self, payload):
        response = requests.post(
            'https://graph.facebook.com/v2.6/me/messenger_profile',
            params={'access_token': MESSENGER['page_access_token']},
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'get_started': {'payload': payload}

            })
        )

        return response.text
