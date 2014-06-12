from pyramid import testing


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

    @classmethod
    def teardown_class(cls):
        testing.tearDown()

    def authenticate(self, user):
        self.config.testing_securitypolicy(userid=user.username)


def match_request(params=None, **kwargs):
    return DummyRequest(matchdict=kwargs, params=params)


def create_rid(name):
    return name.replace(' ', '_')
