import os

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class FTPUserGroup(models.Model):
    name = models.CharField(
        _("Group name"), max_length=30, null=False, blank=False, unique=True)
    permission = models.CharField(
        _("Permission"), max_length=8, null=False, blank=False,
        default='elradfmw')
    home_dir = models.CharField(
        _("Home directory"), max_length=1024, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _("FTP user group")
        verbose_name_plural = _("FTP user groups")


@python_2_unicode_compatible
class FTPUserAccount(models.Model):
    username = models.CharField(
        _("Username"), max_length=64, null=False, blank=False,
        unique=True)
    password = models.CharField(
        _("Password"), max_length=64, null=False, blank=False)
    group = models.ForeignKey(
        FTPUserGroup, verbose_name=_("FTP user group"), null=False,
        blank=False)
    last_login = models.DateTimeField(
        _("Last login"), editable=False, null=True)
    home_dir = models.CharField(
        _("Home directory"), max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username or ""

    def update_last_login(self, value=None):
        self.last_login = value or timezone.now()

    def get_home_dir(self):
        if self.home_dir:
            directory = self.home_dir
        elif self.group:
            directory = self.group.home_dir
        else:
            directory = os.path.join(
                os.path.dirname(os.path.expanduser('~')), '{username}')
        directory = directory.format(username=self.get_username())

        if not os.path.exists(directory):
            os.makedirs(directory)

        return directory

    def has_perm(self, perm, path):
        return perm in self.get_perms()

    def get_perms(self):
        return self.group.permission

    class Meta:
        verbose_name = _("FTP user account")
        verbose_name_plural = _("FTP user accounts")
