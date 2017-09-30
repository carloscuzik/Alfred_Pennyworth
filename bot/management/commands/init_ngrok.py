import os
import json
import socket
from subprocess import Popen, PIPE

import requests
from django.core.management.base import BaseCommand, CommandError

from bots.settings.base import MESSENGER


class Command(BaseCommand):
    """
    Command responsible to boot ngrok and subscribe to
    Facebook Messenger using ngrok's generated URL.
    """

    @staticmethod
    def _check_ngrok_port():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 4040))

        if result == 0:
            raise CommandError('Port 4040 is already being used!')

    @staticmethod
    def _get_ngrok_url():
        response = requests.post(
            'http://localhost:4040/api/tunnels',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'addr': 8000, 'proto': 'http', 'name': 'suster'})
        )

        return response.json()['public_url']

    @staticmethod
    def _get_messenger_access_token():
        url = f"https://graph.facebook.com/oauth/access_token?client_id={MESSENGER['client_id']}" \
               f"&client_secret={MESSENGER['client_secret']}&grant_type=client_credentials"
        response = requests.get(url)

        return response.json()['access_token']

    @staticmethod
    def _update_callback_url_on_messenger(access_token, callback_url):
        url = f"https://graph.facebook.com/v2.9/{MESSENGER['client_id']}/subscriptions?" \
               f'access_token={access_token}'
        data = json.dumps({
            'object': 'page',
            'callback_url': f'{callback_url}/bot/',
            'verify_token': MESSENGER['verify_token'],
            'fields': ['messages', 'messaging_postbacks' , 'message_echoes']
        })
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=data)

        if response.status_code != 200:
            raise CommandError("Can't update callback URL on Facebook's Graph API")

        print("Callback URL successfully updated on Facebook's Graph API")

    def handle(self, *args, **options):
        self._check_ngrok_port()

        command = 'ngrok start --none --log=stdout'.split()
        process = Popen(command, stdout=PIPE, bufsize=1, universal_newlines=True)

        for line in process.stdout:
            print(line, end='')

            if 'client session established' in line:
                callback_url = self._get_ngrok_url()
                access_token = self._get_messenger_access_token()
                self._update_callback_url_on_messenger(access_token, callback_url)
