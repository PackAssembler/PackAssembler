from pyramid.security import authenticated_userid, has_permission
from pyramid.httpexceptions import HTTPFound
from urllib.parse import urlencode
from ..security import Root
from hashlib import md5
from ..schema import *
import requests

CAPTCHA_URL = 'http://www.google.com/recaptcha/api/verify'
CAPTCHA_ERRORS = {
    'invalid-site-private-key': 'Invalid API Key.',
    'invalid-request-cookie': 'The challenge parameter of the verify script ' +
                              'was incorrect.',
    'incorrect-captcha-sol': 'The CAPTCHA solution was incorrect.',
    'captcha-timeout': 'The solution was received after the CAPTCHA timed out.'
}
CAPTCHA_MESSAGE = 'Something went wrong when verifying the Captcha. '
VERROR = 'Your Data is not Valid. Enable Javascript for More Information.'


class ViewBase(object):

    def __init__(self, request):
        self.request = request
        self.logged_in = authenticated_userid(request)
        connect(request.registry.settings.get('mongodb', 'packassembler'))
        self.current_user = User.objects(username=self.logged_in).first()

    def return_dict(self, **kwargs):
        rdict = kwargs
        try:
            rdict['user'] = self.current_user
        except DoesNotExist:
            rdict['user'] = None
        return rdict

    def success_url(self, redirect, message):
        return HTTPFound(location=self.request.route_url('success') + '?' + urlencode({'redirect': redirect, 'message': message}))

    def get_orphan_user(self):
        return User.objects(group="orphan").first()

    def has_perm(self, data):
        dtype = data.__class__.__name__
        if dtype == 'User':
            user = data
        elif dtype == 'ModVersion':
            user = data.mod.owner
        elif dtype == 'PackBuild':
            user = data.pack.owner
        else:
            user = data.owner

        return self.logged_in == user.username or self.specperm('moderator')

    def specperm(self, permission):
        return has_permission(permission, Root, self.request)

    def get_db_object(self, collection, perm=True):
        data = collection.objects.get(id=self.request.matchdict['id'])
        if perm and not self.has_perm(data):
            raise NoPermission
        return data

    def check_depends(self, data):
        dtype = data.__class__.__name__
        if dtype == 'Mod':
            return Pack.objects(mods=data).first() is None
        elif dtype == 'Pack':
            return Server.objects(build__in=data.builds).first() is None
        elif dtype == 'PackBuild':
            return Server.objects(build=data).first() is None
        else:
            return TypeError('Cannot only check dependencies for Mod and Pack types')

    def get_add_pack_data(self):
        if self.logged_in is None:
            return []
        else:
            return Pack.objects(owner=self.current_user).only('id', 'name')


def opt_dict(**kwargs):
    d = {}
    for name, value in kwargs.items():
        if value:
            d[name] = value
        else:
            d[name] = None
    return d


class NoPermission(Exception):
    pass


def validate_captcha(request):
    payload = {
        'privatekey': request.registry.settings.get('recaptcha_priv_key'),
        'remoteip': request.remote_addr,
        'challenge': request.params.get('recaptcha_challenge_field', ''),
        'response': request.params.get('recaptcha_response_field', '')
    }
    t = requests.post(CAPTCHA_URL, payload).text.split('\n')
    try:
        return t[0][0] == 't', CAPTCHA_MESSAGE + CAPTCHA_ERRORS[t[1]]
    except KeyError:
        return t[0][0] == 't', CAPTCHA_MESSAGE + t[1]


def url_md5(url, BLOCKSIZE=16 * 1024):
    hasher = md5()
    req = requests.get(url)
    hasher.update(req.content)
    return hasher.hexdigest(), req.url
