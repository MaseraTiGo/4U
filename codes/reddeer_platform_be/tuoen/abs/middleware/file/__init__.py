# coding=UTF-8

import os
import time
import random
from abs.middleware.extend.oss import OSSAPI
from settings import STATIC_URL, STATIC_FILES_ROOT
from tuoen.sys.utils.common.single import Single


class FileMiddleware(Single):

    @staticmethod
    def get_save_file_name(name):
        names = name.split('.')
        name = "{}_{}.{}".format(
            str(random.randint(1000, 9999)),
            int(time.time()),
            names[-1]
        )
        return name

    def save_local(self, name, f_io, store_type='default'):
        new_name = self.get_save_file_name(name)
        base_dir = STATIC_FILES_ROOT
        save_path = os.path.join(base_dir, store_type)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = os.path.join(save_path, new_name)
        with open(file_path, 'wb') as f:
            f.write(f_io.read())
        url = STATIC_URL + file_path.replace(base_dir, "").replace("\\", "/")
        return url.replace("//", "/")

    def save_oss(self, name, f_io, store_type='default'):
        new_name = "source/{}/{}".format(
            store_type,
            self.get_save_file_name(name)
        )
        image_url = OSSAPI().put_object(new_name, f_io, "reddeer")
        return image_url

    def save(self, name, f_io, store_type, location="local"):
        path = ""
        if location == "local":
            path = self.save_local(name, f_io, store_type)
        elif location == "oss":
            path = self.save_oss(name, f_io, store_type)

        return path


file_middleware = FileMiddleware()
