# coding=utf-8
from __future__ import unicode_literals

from django import forms

from case.models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
