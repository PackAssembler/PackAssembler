
def includeme(config):
    # General
    config.add_route('home', '/')
    config.add_route('faq', '/faq')
    config.add_route('gettingstarted', '/gettingstarted')
    config.add_route('success', '/success')
    config.add_route('error', '/error/{type}')

    # User
    ## Listing
    config.add_route('userlist', '/users')
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
    ## Email
    config.add_route('emailuser', '/users/{id}/email')

    # Mods
    ## Listing
    config.add_route('modlist', '/mods')
    config.add_route('qmlist', '/mods.json')
    ## Spcial Actions
    config.add_route('adoptmod', '/mods/{id}/adopt')
    config.add_route('disownmod', '/mods/{id}/disown')
    config.add_route('flagmod', '/mods/{id}/flag')
    config.add_route('moveversion', '/mods/{id}/moveversion/{index}/{shift}')
    config.add_route('quickmod', '/mods/{id}.json')
    ## Details
    config.add_route('editmodbanner', '/mods/{id}/banner/edit')
    ## CRUD
    config.add_route('addmod', '/mods/add')
    config.add_route('editmod', '/mods/{id}/edit')
    config.add_route('deletemod', '/mods/{id}/delete')
    config.add_route('viewmod', '/mods/{id}')

    # Mod versions
    config.add_route('addversion', '/mods/{id}/versions/add')
    config.add_route('quickadd', '/mods/{id}/versions/quickadd')
    config.add_route('editversion', '/mods/versions/{id}/edit')
    config.add_route('downloadversion', '/mods/versions/{id}/download')
    config.add_route('deleteversion', '/mods/versions/{id}/delete')
    config.add_route('versiondetails', '/mods/versions/{id}')
    config.add_route('qmversions', '/mods/{id}/versions.json')

    # Packs
    ## Listing
    config.add_route('packlist', '/packs')
    ## API
    config.add_route('mcuxmlpack', '/packs/{id}/mcuxml')
    config.add_route('downloadpack', '/packs/{id}/download')
    config.add_route('forgeversions', '/packs/forgeversions')
    ## Details
    config.add_route('editpackbanner', '/packs/{id}/banner/edit')
    ## CRUD
    config.add_route('addpack', '/packs/add')
    config.add_route('clonepack', 'packs/{id}/clone')
    config.add_route('editpack', '/packs/{id}/edit')
    config.add_route('deletepack', '/packs/{id}/delete')
    config.add_route('viewpack', '/packs/{id}')

    ## Mods
    config.add_route('addpackmod', '/packs/{id}/addmod')
    config.add_route('removepackmod', '/packs/{id}/removemod')

    ## Base Packs
    config.add_route('addbasepack', '/packs/{id}/addbase')
    config.add_route('removebasepack', '/packs/{id}/removebase')

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
    ## Details
    config.add_route('editserverbanner', '/servers/{id}/banner/edit')
    ## CRUD
    config.add_route('addserver', '/servers/add')
    config.add_route('editserver', '/servers/{id}/edit')
    config.add_route('deleteserver', '/servers/{id}/delete')
    config.add_route('viewserver', '/servers/{id}')

    config.add_static_view('static', 'static', cache_max_age=3600)
