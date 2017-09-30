import json
import redis

from rivescript.sessions import SessionManager


class RedisSessionStorage(SessionManager):
    def __init__(self, host='localhost', port=6379, password=None, db=0):
        self.client = redis.StrictRedis(host=host, port=port, password=password, db=db)

    def key(self, username, frozen=False):
        """Translate a username into a key for Redis."""
        if frozen:
            return "rs-users-frozen/{}".format(username)
        return "rs-users/{}".format(username)

    def get_user(self, username):
        """Custom method to retrieve a user's data from Redis."""
        data = self.client.get(self.key(username))
        if data is None:
            return None
        return json.loads(data.decode())

    def set(self, username, vars):
        data = self.get_user(username)
        if data is None:
            data = self.default_session()
        data.update(vars)
        self.client.set(self.key(username), json.dumps(data))

    def get(self, username, key):
        data = self.get_user(username)
        if data is None:
            return None
        return data.get(key, 'undefined')

    def get_any(self, username):
        return self.get_user(username)

    def get_all(self):
        users = self.client.keys('rs-users/*')
        result = dict()
        for _user in users:
            username = users.replace('rs-users/', "")
            result[username] = self.get_user(username)
        return result

    def reset(self, username):
        self.client.delete(self.key(username))

    def reset_all(self):
        users = self.client.keys('rs-users/')
        for user in users:
            self.client.delete(user)

    def freeze(self, username):
        data = self.get_user(username)
        if data is not None:
            self.client.set(self.key(username, True), json.dumps(data))

    def thaw(self, username, action='thaw'):
        data = self.client.get(self.key(username, True))
        if data is not None:
            data = json.loads(data.decode())
            if action == 'thaw':
                self.set(username, data)
                self.client.delete(self.key(username, True))
            elif action == 'discard':
                self.client.delete(self.key(username, True))
            elif action == 'keep':
                self.set(username, data)
            else:
                raise ValueError('Unsupported thaw action.')
