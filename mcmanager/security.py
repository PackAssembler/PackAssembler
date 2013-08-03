from pyramid.security import Allow, Everyone
from mongoengine import connect
from .schema import User
import bcrypt


def findgroup(userid, request):
    connect(request.registry.settings.get('mongodb', 'mcmanager'))
    user = User.objects(username=userid).first()
    if user is not None:
        return user.groups


def check_pass(username, password):
    user = User.objects(username=username).first()
    try:
        if user is not None and bcrypt.hashpw(password.encode(), user.password) == user.password:
            return True
        else:
            return False
    except ValueError:
        return True

def password_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Root:
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:user', 'user'),
               (Allow, 'group:admin', 'admin')]

    def __init__(self, request):
        pass
