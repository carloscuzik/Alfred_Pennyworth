import json
from os import environ
from flask import Flask, request
from messenger import MessengerClient
from messenger.content_types import TextMessage

FACEBOOK_VERIFICATION_TOKEN = environ.get('FACEBOOK_VERIFICATION_TOKEN')
FACEBOOK_PAGE_ACCESS_TOKEN = environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')

app = Flask(__name__)
client = MessengerClient(FACEBOOK_PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def handle_verification():
  if request.args.get('hub.verify_token', '') == FACEBOOK_VERIFICATION_TOKEN:
    return request.args.get('hub.challenge', '')

  return 'Error: Invalid verification token'

@app.route('/', methods=['POST'])
def handle_messages():
  print('Message received.')

  message_entries = json.loads(request.data.decode('utf8'))['entry']

  for entry in message_entries:
    for message_data in entry['messaging']:
      print('[INFO] message:', message_data['message']['text'])
      sender_id = message_data['sender']['id']
      client.send(sender_id, TextMessage('Recebi sua mensagem!'))

  return 'OK'

if __name__ == '__main__':
  app.run()