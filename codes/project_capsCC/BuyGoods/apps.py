from django.apps import AppConfig
# from django.db.models.signals import post_save


class BuygoodsConfig(AppConfig):
    name = 'BuyGoods'
    app_label = 'road_buy_goods'

    def ready(self):
        print("=" * 33)
        from BuyGoods.models_store.members import Users
        # Users = self.get_model('Users')
        # from BuyGoods.restful_framework_utils.signals import notification_register_email_test
        # post_save.connect(notification_register_email_test, sender='BuyGoods.Users')
        from BuyGoods.restful_framework_utils.signals import notification_register_email
        print('Buygoods app is ready ro use!')
        # print('fuck you')
        # # notification_register_email()
        print("=" * 33)
