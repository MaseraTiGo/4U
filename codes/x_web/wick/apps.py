import threading

from django.apps import AppConfig

r_lock = threading.RLock()


class WickConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wick'

    def ready(self):
        with r_lock:
            # if redis_sys.get('wick_is_doing'):
            #     return
            # redis_sys.set('wick_is_doing', 1, ex=99)
            from django.conf import settings
            from django.core import management
            from django.db import migrations, ProgrammingError

            from wick.migrate_tools import MigrationsManager
            from wick.app_conf import AppMgmtConf
            from wick.rewrite_cls import MyFuckingMigration

            # --------------- migrate relative things --------------------------
            settings.PRINT_PREFIX = "superDong ---------------->" \
                if not hasattr(settings, 'PRINT_PREFIX') else settings.PRINT_PREFIX

            ori_migration = migrations.Migration
            migrations.Migration = MyFuckingMigration

            # --------------- migrate the migrations 2 db ---------------

            settings.AUTO_MIGRATE_APPS = [
                AppMgmtConf(*args) for args in settings.AUTO_MIGRATE_APPS
            ]

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
                        # 'fake_initial': True,
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
                    try:
                        management.call_command('makemigrations', app.name)
                    except Exception as f:
                        print(f"dong -----------> confused exception: {f}")
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
            try:
                # MigrationsManager.clear_all_store_files()
                make_my_migrations()
                migrate_my_models()
            except Exception as e:
                import traceback
                print(traceback.print_exc())
                print(f"dong -------------> wick, something gets wrong: {e}")
            migrations.Migration = ori_migration

            # migrations.RunPython()
            # redis_sys.delete('wick_is_doing')

            # --------------- migrate relative things --------------------------
