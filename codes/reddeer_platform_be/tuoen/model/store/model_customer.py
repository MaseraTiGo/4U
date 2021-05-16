# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: model_customer
# DateTime: 2020/12/7 17:16
# Project: operate_backend_be
# Do Not Touch Me!


from django.db.models import CASCADE

from model.store.model_user import BaseUser
from model.store.model_company import Company
from model.fields import VirtualForeignKey
from model import AGENT_PREFIX
from model.store.model_forms import Form
from model.store.model_landingpagevent import LandingPage


class Customer(BaseUser):
    """customer table"""

    company = VirtualForeignKey(Company, on_delete=CASCADE, related_name='company_customers', null=True)
    form = VirtualForeignKey(Form, on_delete=CASCADE, related_name='form_customers', null=True)
    landing_page = VirtualForeignKey(LandingPage, on_delete=CASCADE, related_name='landing_page_customers', null=True)

    class Meta:
        db_table = AGENT_PREFIX + 'customer'
