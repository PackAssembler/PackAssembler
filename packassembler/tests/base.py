from pyramid import testing
from copy import copy


class DummyRequest(testing.DummyRequest):
    session = {}

    def flash(self, msg):
        self.session['flash'] = [msg]

    def flash_error(self, msg):
        self.session['error_flash'] = [msg]


class BaseTest:
    def _get_test_class(self):
        pass

    def make_one(self, *args, **kw):
        return self._get_test_class()(*args, **kw)

    @classmethod
    def setup_class(cls):
        cls.config = testing.setUp()
        cls.config.include('packassembler')
        cls.config.include('pyramid_mailer.testing')

    @classmethod
    def teardown_class(cls):
        testing.tearDown()

    def authenticate(self, user):
        self.config.testing_securitypolicy(userid=user.username)


def match_request(params=None, **kwargs):
    return DummyRequest(matchdict=kwargs, params=params)


def create_rid(name):
    return name.replace(' ', '_')


def document_to_data(doc):
    data = copy(doc._data)
    data['submit'] = ''

    filtered = {}
    for k, v in data.items():
        if v is not None:
            filtered[k] = v

    return filtered
