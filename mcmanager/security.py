from pyramid.security import Allow, Everyone
from mongoengine import connect
from .schema import User


def findgroup(userid, request):
    connect(request.registry.settings.get('mongodb', 'mcmanager'))
    user = User.objects(username=userid).first()
    if user is not None:
        return user.groups


def check_pass(username, password):
    user = User.objects(username=username).first()
    if user is not None and user.password.decode() == password:
        return True
    else:
        return False


class Root:
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:user', 'user'),
               (Allow, 'group:admin', 'admin')]

    def __init__(self, request):
        pass
