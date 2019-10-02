from django.apps import AppConfig


class RestfulConfig(AppConfig):
    name = 'restful'

    def ready(self):
        print("I am not fucking ready")
