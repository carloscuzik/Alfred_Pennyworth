import json
import requests

import argparse
from django.core.management.base import BaseCommand
from optparse import make_option

from bots.settings.base import MESSENGER


class Command(BaseCommand):

    help = 'Set up Messenger Persistent Menu'

    def add_arguments(self, parser):
        parser.add_argument('PERSISTENT_MENU_TITLE', action='store', help='User defined  persistent menu title', type=str),
        parser.add_argument('PERSISTENT_MENU_PAYLOAD', action='store', help='User defined persistent menu payload', type=str),

    def handle(self, *args, **options):
        print(self._send_properties(options['PERSISTENT_MENU_TITLE'], options['PERSISTENT_MENU_PAYLOAD']))

    def _send_properties(self, title, payload):
        response = requests.post(
            'https://graph.facebook.com/v2.6/me/messenger_profile',
            params={'access_token': MESSENGER['page_access_token']},
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "persistent_menu":[{
                    "locale":"default",
                    "composer_input_disabled": False,
                    "call_to_actions":[{
                            "title": title,
                            "type":"postback",
                            "payload": payload
                        }]
                    }
                  ,
                  {
                    "locale":"pt_BR",
                    "composer_input_disabled": False
                  }]

            })
        )

        return response.text
