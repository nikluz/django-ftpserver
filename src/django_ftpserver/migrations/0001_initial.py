# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FTPUserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64, verbose_name='Username')),
                ('password', models.CharField(max_length=64, verbose_name='Password')),
                ('last_login', models.DateTimeField(verbose_name='Last login', null=True, editable=False)),
                ('home_dir', models.CharField(max_length=1024, null=True, verbose_name='Home directory', blank=True)),
            ],
            options={
                'verbose_name': 'FTP user account',
                'verbose_name_plural': 'FTP user accounts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FTPUserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='Group name')),
                ('permission', models.CharField(default=b'elradfmw', max_length=8, verbose_name='Permission')),
                ('home_dir', models.CharField(max_length=1024, null=True, verbose_name='Home directory', blank=True)),
            ],
            options={
                'verbose_name': 'FTP user group',
                'verbose_name_plural': 'FTP user groups',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ftpuseraccount',
            name='group',
            field=models.ForeignKey(verbose_name='FTP user group', to='django_ftpserver.FTPUserGroup'),
            preserve_default=True,
        ),
    ]
