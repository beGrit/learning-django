import datetime
import json

import redis


class LoginCode:

    def __init__(self, email: str, code=None, expire_time=None) -> None:
        super().__init__()
        if len(email) == 0:
            raise Exception
        self._input_email = email
        self._input_code = code
        self._input_expire_time = expire_time

    @property
    def email(self):
        return self._input_email

    @property
    def code(self):
        if self._input_code is None:
            return '5678'
        return self._input_code

    @property
    def expire_time(self):
        if self._input_expire_time is None:
            expire_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
            return expire_time
        return self._input_expire_time

    @property
    def key(self):
        return self.email + self.code

    def get(self):
        return {
            'key': self.email,
            'code': self.code,
            'expire_time': str(self.expire_time),
        }

    def persistence(self):
        # Set code message to redis.
        redis_client = redis.Redis()
        redis_client.set(self.key, json.dumps(self.get()))


class LoginCodeRepositoryRedisImpl:
    def save(self, login_code: LoginCode):
        # Set code message to redis.
        redis_client = redis.Redis()
        redis_client.set(login_code['key'], json.dumps(login_code))
