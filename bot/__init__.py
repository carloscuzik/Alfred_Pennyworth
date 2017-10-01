import os

from rivescript import RiveScript
from urllib.parse import urlparse
from .redis_session_storage import RedisSessionStorage

REDIS_URL = os.environ.get('REDIS_URL')

class Bot(object):
    def __init__(self, directory='./conversations', redis_url=REDIS_URL):
        url = urlparse(redis_url)
        session_manager = RedisSessionStorage(
            host=url.hostname,
            port=url.port,
            password=url.password
        )

        self.bot = RiveScript(
            utf8=True,
            session_manager=session_manager
        )
        self.bot.load_directory(directory)
        self.bot.sort_replies()

    def reply(self, sender_id, message):
        return self.bot.reply(sender_id, message)
