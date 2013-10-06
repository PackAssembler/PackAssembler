from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import find_group


def setup_auth(config):
    authn_policy = AuthTktAuthenticationPolicy('authtktpolicysek', callback=find_group, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_authentication_policy(authn_policy)


def setup_tweens(config):
    config.add_tween('packassembler.tweens.exception_tween_factory')


def setup_routes(config):
    # General
    config.add_route('home', '/')
    config.add_route('faq', '/faq')
    config.add_route('gettingstarted', '/gettingstarted')
    config.add_route('success', '/success')
    config.add_route('error', '/error/{type}')

    # User
    ## Signup Process
    config.add_route('signup', '/users/signup')
    config.add_route('activate', '/users/{id}/activate/{key}')
    ## Login/Logout
    config.add_route('login', '/users/login')
    config.add_route('logout', '/users/logout')
    ## Password Reset
    config.add_route('sendreset', '/users/reset')
    config.add_route('reset', '/users/{id}/reset/{key}')
    ## RUD
    config.add_route('edituser', '/users/{id}/edit')
    config.add_route('deleteuser', '/users/{id}/delete')
    config.add_route('profile', '/users/{id}')

    # Mods
    ## Listing
    config.add_route('modlist', '/mods')
    ## Spcial Actions
    config.add_route('adoptmod', '/mods/{id}/adopt')
    config.add_route('disownmod', '/mods/{id}/disown')
    config.add_route('flagmod', '/mods/{id}/flag')
    config.add_route('moveversion', '/mods/{id}/moveversion/{index}/{shift}')
    ## Details
    config.add_route('editbanner', '/mods/{id}/banner/edit')
    ## CRUD
    config.add_route('addmod', '/mods/add')
    config.add_route('editmod', '/mods/{id}/edit')
    config.add_route('deletemod', '/mods/{id}/delete')
    config.add_route('viewmod', '/mods/{id}')

    # Mod versions
    config.add_route('addversion', '/mods/{id}/versions/add')
    config.add_route('editversion', '/mods/versions/{id}/edit')
    config.add_route('downloadversion', '/mods/versions/{id}')
    config.add_route('deleteversion', '/mods/versions/{id}/delete')

    # Packs
    ## Listing
    config.add_route('packlist', '/packs')
    ## API
    config.add_route('mcuxmlpack', '/packs/{id}/mcuxml')
    config.add_route('forgeversions', '/packs/forgeversions')
    ## Technic API
    config.add_route('technic_packlist', '/technic/api/modpack/')
    config.add_route('technic_viewpack', '/technic/api/modpack/{rid}/')
    config.add_route('technic_viewbuild', '/technic/api/modpack/{rid}/{revision}/')
    config.add_route('technic_repo', '/technic/api/repo/{rid}/resources/{image}')
    ## CRUD
    config.add_route('addpack', '/packs/add')
    config.add_route('clonepack', 'packs/{id}/clone')
    config.add_route('editpack', '/packs/{id}/edit')
    config.add_route('deletepack', '/packs/{id}/delete')
    config.add_route('viewpack', '/packs/{id}')

    ## Mods
    config.add_route('addpackmod', '/packs/{id}/addmod')
    config.add_route('removepackmod', '/packs/{packid}/removemod/{modid}')

    ## Builds
    config.add_route('addbuild', '/packs/{id}/builds/add')
    config.add_route('deletebuild', '/packs/builds/{id}/delete')
    config.add_route('downloadbuild', '/packs/builds/{id}')
    config.add_route('mcuxml', '/packs/builds/{id}/mcuxml')
    config.add_route('paq', '/packs/builds/{id}/paq')

    # Servers
    ## Listing
    config.add_route('serverlist', '/servers')
    ## API
    config.add_route('mcuxmlserver', '/servers/{id}/mcuxml')
    ## CRUD
    config.add_route('addserver', '/servers/add')
    config.add_route('editserver', '/servers/{id}/edit')
    config.add_route('deleteserver', '/servers/{id}/delete')
    config.add_route('viewserver', '/servers/{id}')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()


def main(global_config, **settings):
    config = Configurator(settings=settings, root_factory='packassembler.security.Root')
    setup_auth(config)
    setup_tweens(config)
    setup_routes(config)

    return config.make_wsgi_app()
