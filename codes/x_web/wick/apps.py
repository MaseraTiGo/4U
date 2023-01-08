from django.apps import AppConfig


class WickConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wick'

    def ready(self):
        from django.conf import settings
        from wick.migrate_tools import MigrationsManager
        from django.core import management
        from django.db import migrations, ProgrammingError
        from wick.rewrite_cls import MyFuckingMigration

        # --------------- migrate relative things ------------------------------
        settings.PRINT_PREFIX = "superDong ---------------->" \
            if not hasattr(settings, 'PRINT_PREFIX') else settings.PRINT_PREFIX

        ori_migration = migrations.Migration
        migrations.Migration = MyFuckingMigration

        # --------------- migrate the migrations 2 db ---------------

        def migrate_my_models(appoint_app=None, appoint_migration=None):
            for app in sorted(settings.AUTO_MIGRATE_APPS,
                              key=lambda x: x.weight, reverse=True):
                if appoint_app and appoint_app != app.name:
                    continue
                db = settings.DATABASE_APPS_MAPPING.get(app.name)
                if not db:
                    continue
                args = [app.name]
                kwargs = {
                    'fake_initial': True,
                    'database': db
                }
                if appoint_migration:
                    args.append(appoint_migration)
                management.call_command("migrate", *args, **kwargs)
                print(f"{settings.PRINT_PREFIX} {db} migrate successfully!\n")

        # --------------- migrate the migrations 2 db ---------------

        # --------------- make the fucking migrations ---------------

        def make_my_migrations():
            for app in sorted(settings.AUTO_MIGRATE_APPS,
                              key=lambda x: x.weight):
                if not app.store_2_db:
                    management.call_command('makemigrations', app.name)
                    continue

                # generate a migration manager by app.
                cur_app_manager = MigrationsManager(app.name)

                # trans migration files from db.
                try:
                    cur_app_manager.write_2_file_from_db()
                except ProgrammingError:
                    print(f"{settings.PRINT_PREFIX} app: {self.name} "
                          f"has not initialized yet.")
                # get migrations that already exist.
                before_make = cur_app_manager.get_migration_files()
                # make the new migrations
                management.call_command('makemigrations', app.name)
                # get migrations after the remake.
                after_make = cur_app_manager.get_migration_files()
                # find the new migrations.
                new_migrations = set(after_make) - set(before_make)
                # mgmt app's migrations must be applied first.
                if app.name == self.name:
                    migrate_my_models(appoint_app=app.name,
                                      appoint_migration='0001_initial')
                # store new migrations 2 db.
                cur_app_manager.store_migrations_2_db(new_migrations)

        # --------------- make the fucking migrations ---------------

        make_my_migrations()
        migrate_my_models()
        migrations.Migration = ori_migration
        # --------------- migrate relative things ------------------------------
