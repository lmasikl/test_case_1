# coding=utf-8
from __future__ import unicode_literals

from django import http
from django.db import models


class Account(models.Model):
    CURRENCY_CHOICES = (
        ('usd', 'USD'),
        ('rub', 'RUB'),
    )
    BANK_CHOICES = (
        (1, 'РосСтройБанк'),
        (2, 'Тинькофф банк'),
        (3, 'Сбербанк'),
    )
    number = models.IntegerField()
    name = models.CharField(max_length=32)
    account = models.IntegerField()
    bank = models.IntegerField(choices=BANK_CHOICES)
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default='rub'
    )


class Department(models.Model):
    name = models.CharField(max_length=32)
    account = models.OneToOneField(Account)


class Project(models.Model):
    name = models.CharField(max_length=32)
    account = models.OneToOneField(Account)


class Payment(models.Model):
    STATUS_CHOICES = (
        (1, 'Запланированный платеж'),
        (2, 'Совершенный платеж'),
    )
    OPERATION_CHOICES = (
        (1, 'Приход'),
        (2, 'Расход'),
    )
    information = models.TextField()
    account = models.ForeignKey(Account)
    department = models.ForeignKey(Department, blank=True, null=True)
    project = models.ForeignKey(Project, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    operation = models.IntegerField(choices=OPERATION_CHOICES)

    def save(self, *args, **kwargs):
        if self.department and self.project:
            raise http.HttpResponseBadRequest
        return super(Payment, self).save(*args, **kwargs)
