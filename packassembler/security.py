from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone
from mongoengine import connect
from .schema import User
import bcrypt
import hmac


hpass = lambda password: hmac.new(password.encode()).digest()


def includeme(config):
    authn_policy = AuthTktAuthenticationPolicy('authtktpolicysek',
                                               callback=find_group,
                                               hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_authentication_policy(authn_policy)


def find_group(userid, request):
    connect('', host=request.registry.settings.get('mongodb', 'packassembler'))
    user = User.objects(username=userid).first()
    if user is not None:
        return ['group:' + user.group]


def check_pass(username, password):
    if '@' in username:
        user = User.objects(email=username).first()
    else:
        user = User.objects(username=username).first()

    try:
        password_correct = bcrypt.hashpw(hpass(password), user.password) == user.password
    except AttributeError:
        return False

    if password_correct and user.activate is None:
        if user.reset:
            user.reset = None
            user.save()
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
