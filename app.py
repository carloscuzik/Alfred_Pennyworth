import os
import json
import unidecode

from flask import Flask, request
from messenger import MessengerClient
from messenger.content_types import TextMessage
from bot import Bot

FACEBOOK_PAGE_TOKEN = os.environ.get('FACEBOOK_PAGE_TOKEN')
FACEBOOK_VERIFICATION_TOKEN = os.environ.get('FACEBOOK_VERIFICATION_TOKEN')

app = Flask(__name__)
bot = Bot()
client = MessengerClient(FACEBOOK_PAGE_TOKEN)

@app.route('/', methods=['GET'])
def handle_verification():
    print('Iniciando a Verificação.')
    if request.args.get('hub.verify_token', '') == FACEBOOK_VERIFICATION_TOKEN:
        print('Verificação bem sucedida!')
        return request.args.get('hub.challenge', '')

    print('Falha na Verificação!')
    return 'Erro, Token de Validação não Confere'

@app.route('/', methods=['POST'])
def handle_messages():
    message_entries = json.loads(request.data.decode('utf8'))['entry']

    for entry in message_entries:
        for message in entry['messaging']:
            sender_id = message['sender']['id']
            if message.get('message'):
                print('[INFO] message:', message)
                text = unidecode.unidecode(message['message']['text'])
                reply = bot.reply(sender_id, text)
                print('[INFO] reply:', reply)
                client.send(sender_id, TextMessage(reply))
            elif message.get('postback'):
                if message['postback'].get('referral'):
                    if message['postback']['referral']['ref'] == 'palestra-bots':
                        print('[INFO] message:', message['postback']['referral']['ref'])
            elif message.get('referral'):
                if message['referral']['ref'] == 'palestra-bots':
                    print('[INFO] message:', message['referral']['ref'])
    return 'OK'

if __name__ == '__main__':
    app.run()
