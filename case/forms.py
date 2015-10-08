# coding=utf-8
from __future__ import unicode_literals

from django import forms

from case.models import Account, Department, Payment, Project


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'