from pyramid.security import authenticated_userid, has_permission
from pyramid.httpexceptions import HTTPFound
from urllib.parse import urlencode
from ..security import Root
from ..schema import *
import requests

CAPTCHA_URL = 'http://www.google.com/recaptcha/api/verify'
CAPTCHA_KEY = '6LfMiuUSAAAAACSvxehnpk8IvIOwYZiSuJg58oa2'
CAPTCHA_ERRORS = {
    'invalid-site-private-key': 'Invalid API Key.',
    'invalid-request-cookie': 'The challenge parameter of the verify script was incorrect.',
    'incorrect-captcha-sol': 'The CAPTCHA solution was incorrect.',
    'captcha-timeout': 'The solution was received after the CAPTCHA timed out.'
}
CAPTCHA_MESSAGE = 'Something Went Wrong When Verifying the Captcha. '
VERROR = 'Your Data is not Valid. Enable Javascript for More Information.'

class MMLServerView(object):
    def __init__(self, request):
        self.request = request
        self.logged_in = authenticated_userid(request)
        connect(request.registry.settings.get('mongodb', 'mcmanager'))

    def return_dict(self, **kwargs):
        rdict = kwargs
        try:
            rdict['user'] = User.objects.get(username=self.logged_in)
        except DoesNotExist:
            rdict['user'] = None
        return rdict

    def success_url(self, redirect, message):
        return HTTPFound(location=self.request.route_url('success') + '?' + urlencode({'redirect': redirect, 'message': message}))

    def get_orphan_user(self):
        return User.objects.get(username="Orphan")

    def has_perm(self, data, is_user=False):
        if is_user:
            username = data.username
        else:
            username = data.owner.username

        return self.logged_in == username or has_permission('admin', Root, self.request)

    def get_db_object(self, collection, did, perm=True):
        # Overwritten in MMLServerUser
        data = collection.objects.get(id=did)
        if perm and not self.has_perm(data):
            raise NoPermission
        return data


def opt_dict(**kwargs):
    d = {}
    for name, value in kwargs.items():
        if value != '':
            d[name] = value
    return d

class NoPermission(Exception):
    pass

def validate_captcha(request, challenge, response):
    payload = {
        'privatekey': CAPTCHA_KEY,
        'remoteip': request.remote_addr,
        'challenge': challenge,
        'response': response
    }
    t = requests.post(CAPTCHA_URL, payload).text.split('\n')
    try:
        return t[0][0] == 't', CAPTCHA_MESSAGE + CAPTCHA_ERRORS[t[1]]
    except KeyError:
        return t[0][0] == 't', CAPTCHA_MESSAGE + t[1]
