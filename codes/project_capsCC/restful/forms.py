# -*- coding: utf-8 -*-
# file_name       : forms.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/10/21 9:06

from django import forms


class FileUpload(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
