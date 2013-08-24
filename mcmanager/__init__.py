from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import find_group


def main(global_config, **settings):
    config = Configurator(settings=settings, root_factory='mcmanager.security.Root')
    authn_policy = AuthTktAuthenticationPolicy('authtktpolicysek', callback=find_group, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_tween('mcmanager.tweens.exception_tween_factory')

    # General
    config.add_route('home', '/')
    config.add_route('faq', '/faq')
    config.add_route('gettingstarted', '/gettingstarted')
    config.add_route('success', '/success')
    config.add_route('error', '/error/{type}')

    # User
    ## Signup Process
    config.add_route('signup', '/user/signup')
    config.add_route('activate', '/user/activate/{id}/{key}')
    ## Login/Logout
    config.add_route('login', '/user/login')
    config.add_route('logout', '/user/logout')
    ## Password Reset
    config.add_route('sendreset', '/user/reset')
    config.add_route('reset', '/user/reset/{id}/{key}')
    ## RUD
    config.add_route('edituser', '/user/edit/{id}')
    config.add_route('deleteuser', '/user/delete/{id}')
    config.add_route('profile', '/user/{id}')

    # Mods
    ## Listing
    config.add_route('modlist', '/mod/list')
    ## Spcial Actions
    config.add_route('adoptmod', '/mod/adopt/{id}')
    config.add_route('disownmod', '/mod/disown/{id}')
    config.add_route('flagmod', '/mod/flag/{id}')
    ## CRUD
    config.add_route('addmod', '/mod/add')
    config.add_route('editmod', '/mod/edit/{id}')
    config.add_route('deletemod', '/mod/delete/{id}')
    config.add_route('viewmod', '/mod/{id}')

    # Mod versions
    config.add_route('addversion', '/mod/addversion/{id}')
    config.add_route('editversion', '/mod/editversion/{id}')
    config.add_route('downloadversion', '/mod/download/{id}')
    config.add_route('deleteversion', '/mod/deleteversion/{id}')

    # Packs
    ## Listing
    config.add_route('packlist', '/pack/list')
    ## API
    config.add_route('packjson', '/pack/json/{id}')
    ## CRUD
    config.add_route('addpack', '/pack/add')
    config.add_route('editpack', '/pack/edit/{id}')
    config.add_route('deletepack', '/pack/delete/{id}')
    config.add_route('viewpack', '/pack/{id}')

    ## Mods
    config.add_route('addpackmod', '/pack/addmod/{id}')
    config.add_route('removepackmod', '/pack/removemod/{packid}/{modid}')

    ## Builds
    config.add_route('addbuild', '/pack/addbuild/{id}')
    config.add_route('removebuild', '/pack/removebuild/{id}')
    config.add_route('downloadbuild', '/pack/download/{id}')

    # Servers
    ## Listing
    config.add_route('serverlist', '/server/list')
    ## API
    config.add_route('serverjson', '/server/json/{id}')
    ## CRUD
    config.add_route('addserver', '/server/add')
    config.add_route('editserver', '/server/edit/{id}')
    config.add_route('deleteserver', '/server/delete/{id}')
    config.add_route('viewserver', '/server/{id}')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    return config.make_wsgi_app()
