from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from .common import MMLServerView, opt_dict
from pyramid.view import view_config
from ..schema import *
import re


class MMLServerMod(MMLServerView):
    @view_config(route_name='addmod', renderer='editmod.mak', permission='user')
    def addmod(self):
        # Renderer defaults
        error = ''
        # Form
        post = self.request.params
        if 'btnSubmit' in post:
            params = get_params(post)
            if re.match('^[\w ]+$', params['name']) and params['install'].isalnum():
                try:
                    mod = Mod(owner=User.objects.get(username=self.logged_in), **params).save()
                    return HTTPFound(location=self.request.route_url('viewmod', modid=mod.id))
                except ValidationError:
                    error = 'Your data could not be validated. Enable javascript for more information.'
            else:
                error = 'Your mod name must be alphanumeric (with spaces) and your install location must be alphanumeric (no spaces)'
        return self.return_dict(title='Add Mod', error=error)

    @view_config(route_name='editmod', renderer='editmod.mak', permission='user')
    def editmod(self):
        # Renderer defaults
        error = ''
        # Form
        post = self.request.params
        # Get mod
        mod = Mod.objects.get(id=self.request.matchdict['modid'])
        if mod is None:
            return HTTPFound(self.request.route_url('modlist'))
        if 'btnSubmit' in post:
            params = get_params(post)
            if re.match('^[\w ]+$', params['name']) and params['install'].isalnum():
                try:
                    for key in params:
                        if mod[key] != params[key]:
                            mod[key] = params[key]
                    mod.save()
                    return HTTPFound(location=self.request.route_url('viewmod', modid=mod.id))
                except ValidationError:
                    error = 'Your data could not be validated. Enable javascript for more information.'
            else:
                error = 'Your mod name must be alphanumeric (with spaces) and your install location must be alphanumeric (no spaces)'
        return self.return_dict(title='Add Mod', error=error, v=mod)

    @view_config(route_name='modlist', renderer='modlist.mak')
    def modlist(self):
        return self.return_dict(title='Mod List', mods=Mod.objects)

    @view_config(route_name='deletemod', permission='user')
    def deletemod(self):
        mod = Mod.objects.get(id=self.request.matchdict['modid'])
        if mod is None or not self.has_perm(mod):
            return HTTPNotFound()
        else:
            name = mod.name
            for version in mod.versions:
                version.mod_file.delete()
                version.delete()
            mod.delete()
            return self.success_url('modlist', name + ' deleted successfully.')

    @view_config(route_name='viewmod', renderer='viewmod.mak')
    def viewmod(self):
        mod = Mod.objects.get(id=self.request.matchdict['modid'])
        if mod is None:
            return HTTPNotFound()
        else:
            return self.return_dict(title=mod.name, mod=mod, perm=self.has_perm(mod))


def get_params(post):
    return opt_dict(
        name=post.get('txtName'),
        install=post.get('txtInstall'),
        url=post.get('txtUrl'),
        target=post.get('selTarget'),
        permission=post.get('parPermission')
    )
