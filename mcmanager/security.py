from pyramid.security import Allow, Everyone
from mongoengine import connect
from .schema import User
import bcrypt
import hmac


def findgroup(userid, request):
    connect(request.registry.settings.get('mongodb', 'mcmanager'))
    user = User.objects(username=userid).first()
    if user is not None:
        return user.groups


hpass = lambda password: hmac.new(password.encode()).digest()

def check_pass(username, password):
    user = User.objects(username=username).first()
    if user is not None and bcrypt.hashpw(hpass(password), user.password) == user.password and user.activate is None:
        return True
    else:
        return False

def password_hash(password):
    return bcrypt.hashpw(hpass(password), bcrypt.gensalt())


class Root:
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:user', 'user'),
               (Allow, 'group:admin', 'admin')]

    def __init__(self, request):
        pass
