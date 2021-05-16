# coding=UTF-8
import json
import time
from tuoen.sys.utils.cache.redis import redis


class BaseRole(object):
    _category = 'role'

    def get_flag(self):
        flag_name = self.get_role_model().__name__.lower()
        return flag_name

    def _loading(self):
        self._loading_time = time.time()
        agent_role_qs = self.get_role_model().search()
        for role in agent_role_qs:
            self.set_redis(role)

    def is_refresh(self, seconds=5 * 60):
        return (time.time() - self._loading_time) > seconds

    def set_redis(self, role):
        redis_name = self.get_redis_name(role.id)
        redis.set(redis_name, json.dumps(role.rules), self._category)

    def get_redis_name(self, role_id):
        redis_name = "{f}_{r}".format(
            f=self.get_flag(),
            r=str(role_id),
        )
        return redis_name

    def get_redis(self, role_id):
        if not hasattr(self, '_loading_time') or self.is_refresh:
            self._loading()
        try:
            redis_name = self.get_redis_name(role_id)
            value = redis.get(redis_name, self._category)
            if not value:
                role = self.get_role(role_id)
                self.set_redis(role)
        except Exception as e:
            print("====>>>>>redis", e)
            role = self.get_role(role_id)
            self.set_redis(role)
        value = redis.get(redis_name, self._category)
        return value

    def delete_redis(self, role_id):
        redis_name = self.get_redis_name(role_id)
        redis.delete(redis_name)

    def get_role(self, id):
        role = self.get_role_model().get_byid(id)
        return role
