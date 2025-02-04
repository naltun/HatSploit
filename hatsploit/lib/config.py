"""
MIT License

Copyright (c) 2020-2022 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import pathlib
import yaml

from hatsploit.lib.storage import GlobalStorage
from hatsploit.lib.storage import LocalStorage


class Config:
    def __init__(self):
        self.local_storage = LocalStorage()

        self.user_path = f'{pathlib.Path.home()}/.hsf/'
        self.base_path = f'{os.path.dirname(os.path.dirname(__file__))}/'

        self.config_path = self.base_path + 'config/'

        self.db_config_file = self.config_path + 'db_config.yml'
        self.core_config_file = self.config_path + 'core_config.yml'

        self.db_config = self.local_storage.get("db_config")
        self.path_config = {
            'user_path': self.user_path,

            'loot_path': f'{self.user_path}loot/',
            'db_path': f'{self.user_path}db/',

            'accept_path': f'{self.user_path}accept',
            'history_path': f'{self.user_path}history',
            'startup_path': f'{self.user_path}startup.hsf',

            'root_path': self.base_path,

            'data_path': f'{self.base_path}data/',
            'policy_path': f'{self.base_path}data/policy/',
            'tips_path': f'{self.base_path}data/tips/',
            'banners_path': f'{self.base_path}data/banners/',
            'wordlists_path': f'{self.base_path}data/wordlists/',
            'exploits_path': f'{self.base_path}data/exploits/',

            'modules_path': f'{self.base_path}modules/',
            'plugins_path': f'{self.base_path}plugins/',
            'commands_path': f'{self.base_path}commands/',
            'payloads_path': f'{self.base_path}payloads/',
            'encoders_path': f'{self.base_path}encoders/',

            'storage_path': f'{self.base_path}config/storage.json'
        }

        self.core_config = self.local_storage.get("core_config")

    @staticmethod
    def get_config_file(content):
        return yaml.safe_load(content)

    def configure(self):
        db_config = self.get_config_file(open(self.db_config_file))
        core_config = self.get_config_file(open(self.core_config_file))

        self.db_config = db_config
        self.core_config = core_config

        self.local_storage.set("db_config", self.db_config)
        self.local_storage.set("core_config", self.core_config)

        self.global_storage = GlobalStorage(self.path_config['storage_path'])
        self.global_storage.set_all()
