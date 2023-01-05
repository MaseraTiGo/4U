# -*- coding: utf-8 -*-
# @File    : migrate_tools
# @Project : x_web
# @Time    : 2023/1/4 15:54
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import os
import pathlib
import sys
from collections import defaultdict
from functools import partial
from typing import Set

from djangoProject import settings
from wick.models import Migrations


class MigrationNameDuplicateError(Exception):
    pass


class MigrationsManager(object):
    Model = Migrations
    BaseDir = settings.BASE_DIR

    def __init__(self, app, migrations_dir='migrations'):
        self.app = app
        self.migrations_dir = migrations_dir
        self.new_migrations = None

    def get_migration_files(self):
        sep = os.sep
        migration_files = pathlib.Path(f'{self.BaseDir}{sep}').glob(
            f'**{sep}{self.app}{sep}**{sep}{self.migrations_dir}{sep}*.py'
        )
        return [file for file in migration_files if '__init' not in file.stem]

    def store_migrations_2_db(self, migrations):
        if len(set(migrations)) != len(migrations):
            raise MigrationNameDuplicateError(
                f'App: {self.app} has duplicate migrations.'
            )

        self._store_helper(migrations)
        self.new_migrations = migrations

    def _store_helper(self, migrations, block_size=10240):
        for migration in migrations:
            with open(migration) as shit:
                index = 0
                for block in iter(partial(shit.read, block_size), ''):
                    self.Model.objects.create(
                        name=migration.name,
                        content=block,
                        app=self.app,
                        path=str(migration),
                        index=index
                    )
                    index += 1

    def write_2_file_from_db(self):
        migration_qs = self.Model.objects.filter(app=self.app)
        file_mapping = defaultdict(set)
        for migration in migration_qs:
            p_migration = pathlib.Path(migration.path)
            if p_migration.exists():
                if sys.platform == 'win32':
                    os.remove(migration.path)
                else:
                    p_migration.unlink()
            file_mapping[migration.name].add(migration)

        for migrations in file_mapping.values():
            self._write_helper(migrations)

    @staticmethod
    def _write_helper(migrations: Set[Migrations]):
        migrations = sorted(migrations, key=lambda x: x.index)
        for migration in migrations:
            with open(migration.path, 'a') as fuck:
                fuck.write(migration.content)
