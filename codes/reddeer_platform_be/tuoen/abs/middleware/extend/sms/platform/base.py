# coding=UTF-8


class SMSPlatform(object):
    label = None

    def __init__(self, controller, config):
        self.controller = controller
        self.templates = config.use_templates
        self.config = config
