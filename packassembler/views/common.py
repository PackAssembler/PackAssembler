from pyramid.security import authenticated_userid, has_permission
from pyramid.httpexceptions import HTTPFound
from urllib.parse import urlencode
from ..security import Root
from hashlib import md5
from ..schema import *
import requests
import math

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
        self.logged_in = request.authenticated_userid
        connect('', host=request.registry.settings.get('mongodb', 'packassembler'))
        self.current_user = User.objects(username=self.logged_in).first()

    def return_dict(self, **kwargs):
        rdict = kwargs
        try:
            rdict['user'] = self.current_user
        except DoesNotExist:
            rdict['user'] = None
        return rdict

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

        return (user is not None and
                self.logged_in == user.username or
                self.specperm('moderator'))

    def specperm(self, permission):
        return has_permission(permission, Root, self.request)

    def get_db_object(self, collection, perm=True):
        try:
            data = collection.objects.get(id=self.request.matchdict['id'])
        except ValidationError:
            raise DoesNotExist
        if perm and not self.has_perm(data):
            raise NoPermission
        return data

    def check_depends(self, data):
        dtype = data.__class__.__name__
        if dtype == 'Mod':
            return Pack.objects(mods=data).first() is None
        elif dtype == 'ModVersion':
            return PackBuild.objects(mod_versions=data).first() is None
        else:
            return TypeError('Cannot only check dependencies for Mod types')

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


def url_md5(url):
    """ Returns MD5 of file at url. """
    hasher = md5()
    req = requests.get(url)
    hasher.update(req.content)
    # Also return the end url, in case of redirect
    return hasher.hexdigest(), req.url


def slugify(text):
    return text.lower().replace(' ', '-')


def page_list(post, objs):
    per_page = 20

    page = int(post['page']) if 'page' in post else 1
    if page < 1:
        page = 1

    start = (page-1) * per_page

    l = objs.skip(start).limit(per_page)
    assert len(l) == per_page
    return l
