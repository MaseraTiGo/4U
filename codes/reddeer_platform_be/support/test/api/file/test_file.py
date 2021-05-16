# coding=UTF-8

import json
import os
from support.common.testcase.file_api_test_case import FileAPITestCase


class TestFile(FileAPITestCase):

    def test_file_upload(self):
        api = 'file/upload'
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, 'little_boy.png')
        files = {'little_boy_1.jpg': open(file_path, 'rb')}
        result = self.access_api(
            api=api,
            files=files,
            store_type="images"
        )
        print('\n', result)
