from pyramid.security import authenticated_userid, has_permission
from pyramid.httpexceptions import HTTPFound
from urllib.parse import urlencode
from ..security import Root
from ..schema import *


class MMLServerView(object):
    def __init__(self, request):
        self.request = request
        self.logged_in = authenticated_userid(request)
        connect(request.registry.settings.get('mongodb', 'mmlserver'))

    def return_dict(self, **kwargs):
        rdict = kwargs
        try:
            rdict['user'] = User.objects.get(username=self.logged_in)
        except DoesNotExist:
            rdict['user'] = None
        return rdict

    def success_url(self, redirect, message):
        return HTTPFound(location=self.request.route_url('success') + '?' + urlencode({'redirect': redirect, 'message': message}))

    def has_perm(self, data, is_user=False):
        if is_user:
            username = data.username
        else:
            username = data.owner.username

        return self.logged_in == username or has_permission('admin', Root, self.request)

    def get_orphan_user(self):
        return User.objects.get(username="Orphan")


def opt_dict(**kwargs):
    d = {}
    for name, value in kwargs.items():
        if value != '':
            d[name] = value
    return d

VERROR = "Your Data is not Valid. Enable Javascript for More Information."
