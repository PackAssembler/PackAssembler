from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import findgroup


def main(global_config, **settings):
    config = Configurator(settings=settings, root_factory='mcmanager.security.Root')
    authn_policy = AuthTktAuthenticationPolicy('authtktpolicysek', callback=findgroup, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_tween('mcmanager.tweens.exception_tween_factory')
    # General
    config.add_route('home', '/')
    config.add_route('about', '/about')
    config.add_route('gettingstarted', '/gettingstarted')
    config.add_route('success', '/success')
    # User
    config.add_route('signup', '/user/signup')
    config.add_route('taken', '/user/taken')
    config.add_route('login', '/user/login')
    config.add_route('logout', '/user/logout')
    config.add_route('edituser', '/user/edit/{userid}')
    config.add_route('deleteuser', '/user/delete/{userid}')
    config.add_route('profile', '/user/{userid}')
    # Mods
    config.add_route('addmod', '/mod/add')
    config.add_route('editmod', '/mod/edit/{modid}')
    config.add_route('modlist', '/mod/list')
    config.add_route('deletemod', '/mod/delete/{modid}')
    config.add_route('viewmod', '/mod/{modid}')
    # Mod versions
    config.add_route('addversion', '/mod/addversion/{modid}')
    config.add_route('editversion', '/mod/editversion/{versionid}')
    config.add_route('downloadversion', '/mod/download/{versionid}')
    config.add_route('deleteversion', '/mod/deleteversion/{versionid}')
    # Packs
    ## General
    config.add_route('addpack', '/pack/add')
    config.add_route('editpack', '/pack/edit/{packid}')
    config.add_route('packlist', '/pack/list')
    config.add_route('deletepack', '/pack/delete/{packid}')
    config.add_route('viewpack', '/pack/{packid}')
    config.add_route('packjson', '/pack/json/{packid}')
    ## Mods
    config.add_route('addpackmod', '/pack/addmod/{packid}')
    config.add_route('removepackmod', '/pack/removemod/{packid}/{modid}')
    ## Builds
    config.add_route('addbuild', '/pack/addbuild/{packid}')
    config.add_route('removebuild', '/pack/removebuild/{buildid}')
    config.add_route('downloadbuild', '/pack/download/{buildid}')
    # Servers
    config.add_route('addserver', '/server/add')
    config.add_route('editserver', '/server/edit/{serverid}')
    config.add_route('serverlist', '/server/list')
    config.add_route('deleteserver', '/server/delete/{serverid}')
    config.add_route('viewserver', '/server/{serverid}')
    config.add_route('serverjson', '/server/json/{serverid}')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    return config.make_wsgi_app()
