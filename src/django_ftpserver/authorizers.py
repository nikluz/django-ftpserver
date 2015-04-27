import os
import pwd

from pyftpdlib.authorizers import AuthenticationFailed

from . import models
from psycopg2 import OperationalError, InterfaceError
from django.conf import settings


class FTPAccountAuthorizer(object):
    """Authorizer class by django authentication.
    """
    model = models.FTPUserAccount

    def __init__(self, file_access_user=None):
        self.file_access_user = file_access_user
        self.gid = os.getgid()
        self.uid = os.getuid()

    def has_user(self, username):
        """return True if exists user.
        """
        return self.model.objects.filter(username=username).exists()

    def get_account(self, username, password=None):
        """return user by username.
        """
        try:
            if password is None:
                account = self.model.objects.get(username=username)
            else:
                account = self.model.objects.get(username=username,
                                                 password=password)
        except self.model.DoesNotExist:
            return None
        return account

    def validate_authentication(self, username, password, handler):
        """authenticate user with password
        """
        try:
            account = self.get_account(username=username, password=password)
        except (OperationalError, InterfaceError):
            cmd = "cd ~ && source %s && \
                   cd %s && kill $(ps aux | grep '[p]ython \
                   ./manage.py ftpserver' | awk '{print $2}') && ./manage.py \
                   ftpserver %s:%s --daemonize" % (settings.ENV_PATH,
                                                   settings.PRJ_PATH,
                                                   settings.FTP_IP,
                                                   settings.FTP_PORT)
            os.system(cmd)
        if not account:
            raise AuthenticationFailed("Authentication failed.")

    def get_home_dir(self, username):
        account = self.get_account(username)
        if not account:
            return ''
        return account.get_home_dir()

    def get_msg_login(self, username):
        """message for welcome.
        """
        account = self.get_account(username)
        if account:
            account.update_last_login()
            account.save()
        return 'welcome.'

    def get_msg_quit(self, username):
        return 'good bye.'

    def has_perm(self, username, perm, path=None):
        """check user permission
        """
        account = self.get_account(username)
        return account and account.has_perm(perm, path)

    def get_perms(self, username):
        """return user permissions
        """
        account = self.get_account(username)
        return account and account.get_perms()

    def impersonate_user(self, username, password):
        """impersonate user when operating file system
        """
        if self.file_access_user:
            uid = pwd.getpwnam(self.file_access_user).pw_uid
            gid = pwd.getpwnam(self.file_access_user).pw_gid
            os.setegid(gid)
            os.seteuid(uid)

    def terminate_impersonation(self, username):
        """undo user from impersonation
        """
        if self.file_access_user:
            os.setegid(self.gid)
            os.seteuid(self.uid)
