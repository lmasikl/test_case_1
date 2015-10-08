# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=32)),
                ('account', models.IntegerField()),
                ('bank', models.IntegerField(choices=[(1, '\u0420\u043e\u0441\u0421\u0442\u0440\u043e\u0439\u0411\u0430\u043d\u043a'), (2, '\u0422\u0438\u043d\u044c\u043a\u043e\u0444\u0444 \u0431\u0430\u043d\u043a'), (3, '\u0421\u0431\u0435\u0440\u0431\u0430\u043d\u043a')])),
                ('currency', models.CharField(default='rub', max_length=3, choices=[('usd', 'USD'), ('rub', 'RUB')])),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('account', models.OneToOneField(to='case.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('information', models.TextField()),
                ('comment', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, '\u0417\u0430\u043f\u043b\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u043f\u043b\u0430\u0442\u0435\u0436'), (2, '\u0421\u043e\u0432\u0435\u0440\u0448\u0435\u043d\u043d\u044b\u0439 \u043f\u043b\u0430\u0442\u0435\u0436')])),
                ('operation', models.IntegerField(choices=[(1, '\u041f\u0440\u0438\u0445\u043e\u0434'), (2, '\u0420\u0430\u0441\u0445\u043e\u0434')])),
                ('account', models.ForeignKey(to='case.Account')),
                ('department', models.ForeignKey(blank=True, to='case.Department', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('account', models.OneToOneField(to='case.Account')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='project',
            field=models.ForeignKey(blank=True, to='case.Project', null=True),
        ),
    ]
