# -*- coding: utf-8 -*-
# @File    : wick_preset_001
# @Project : x_web
# @Time    : 2023/1/10 14:18
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

from django.db import migrations

from wick.migrate_tools import PresetEntrance


class PresetTest(PresetEntrance):

    def fuck_it(self, apps, schema):
        model = apps.get_model('super_dong', 'Test')
        model.create(name='aston-martin', age=123, sexy=True)


class Migration(migrations.Migration):
    dependencies = [
        ('wick', '0001_initial')
    ]

    operations = [
        migrations.RunPython(PresetTest)
    ]
