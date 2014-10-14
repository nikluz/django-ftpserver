# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def set_default_group(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FTPUserGroup = apps.get_model("django_ftpserver", "FTPUserGroup")
    group = FTPUserGroup(name='default', permission='elradfmw')
    group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('django_ftpserver', '0002_auto_20141014_1150'),
    ]

    operations = [
        migrations.RunPython(set_default_group),
    ]
