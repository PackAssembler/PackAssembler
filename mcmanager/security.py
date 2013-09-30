from pyramid.security import Allow, Everyone
from mongoengine import connect
from .schema import User
import bcrypt
import hmac


hpass = lambda password: hmac.new(password.encode()).digest()


def find_group(userid, request):
    connect(request.registry.settings.get('mongodb', 'mcmanager'))
    user = User.objects(username=userid).first()
    if user is not None:
        return ['group:' + user.group]


def check_pass(username, password):
    if '@' in username:
        user = User.objects(email=username).first()
    else:
        user = User.objects(username=username).first()
    password_correct = bcrypt.hashpw(hpass(password), user.password) == user.password
    if user is not None and password_correct and user.activate is None:
        return user.username
    else:
        return False


def password_hash(password):
    return bcrypt.hashpw(hpass(password), bcrypt.gensalt())


class Root(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'group:user', 'user'),
        (Allow, 'group:contributor', ('user', 'contributor')),
        (Allow, 'group:moderator', ('user', 'contributor', 'moderator')),
        (Allow, 'group:admin', ('user', 'contributor', 'moderator', 'admin'))
    ]

    def __init__(self, request):
        pass
