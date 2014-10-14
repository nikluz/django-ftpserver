# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_ftpserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ftpuseraccount',
            name='username',
            field=models.CharField(unique=True, max_length=64, verbose_name='Username'),
        ),
    ]
