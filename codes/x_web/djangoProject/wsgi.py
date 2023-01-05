"""
WSGI config for djangoProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

from djangoProject import FRAME_PREFIX
from wick.migrate_tools import MigrationsManager

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

application = get_wsgi_application()

# =============== command need to be executed before app starts ================
from django.core import management

# --------------- migrate relative things --------------------------------------
from django.db import migrations, ProgrammingError
from djangoProject.rewrite_cls import MyFuckingMigration

ori_migration = migrations.Migration
migrations.Migration = MyFuckingMigration


# --------------- migrate the migrations 2 db ---------------

def migrate_my_models(appoint_app=None, appoint_migration=None):
    for app, _ in sorted(settings.AUTO_MIGRATE_APPS, key=lambda x: x[-1], reverse=True):
        if appoint_app and appoint_app != app:
            continue
        db = settings.DATABASE_APPS_MAPPING.get(app)
        if not db:
            continue
        # dbs = settings.DATABASE_APPS_MAPPING.items()
        # for app, db in dbs:
        args = [app]
        kwargs = {
            'fake_initial': True,
            'database': db
        }
        if appoint_migration:
            args.append(appoint_migration)
        management.call_command("migrate", *args, **kwargs)
        print(f"{FRAME_PREFIX} {db} migrate successfully!\n")


# --------------- migrate the migrations 2 db ---------------

# --------------- make the fucking migrations ---------------


def make_my_migrations(migration_mgmt_app=settings.MIGRATION_MGMT_APP):
    for app, _ in sorted(settings.AUTO_MIGRATE_APPS, key=lambda x: x[-1]):
        # generate a migration manager by app.
        cur_app_manager = MigrationsManager(app)

        # trans migration files from db.
        try:
            cur_app_manager.write_2_file_from_db()
        except ProgrammingError:
            print(f"{FRAME_PREFIX} app: {migration_mgmt_app} "
                  f"has not initialized yet.")
        # get migrations that already exist.
        before_make = cur_app_manager.get_migration_files()
        # make the new migrations
        management.call_command('makemigrations', app)
        # get migrations after the remake.
        after_make = cur_app_manager.get_migration_files()
        # find the new migrations.
        new_migrations = set(after_make) - set(before_make)
        # mgmt app's migrations must be applied first.
        if app == migration_mgmt_app:
            migrate_my_models(appoint_app=app, appoint_migration='0001_initial')
        # store new migrations 2 db.
        cur_app_manager.store_migrations_2_db(new_migrations)


# --------------- make the fucking migrations ---------------


make_my_migrations()
migrate_my_models()
migrations.Migration = ori_migration
# --------------- migrate relative things --------------------------------------
# =============== command need to be executed before app starts ================

print(f"{FRAME_PREFIX} now, fucking hit me!")
