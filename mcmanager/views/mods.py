from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from ..schema import *
from .common import *
import re


class MMLServerMod(MMLServerView):
    @view_config(route_name='addmod', renderer='editmod.mak', permission='user')
    def addmod(self):
        error = ''
        post = self.request.params

        if 'btnSubmit' in post:
            params = get_params(post)
            if check_params(params):
                try:
                    mod = Mod(owner=User.objects.get(username=self.logged_in), **params).save()
                    return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))
                except ValidationError:
                    error = VERROR
            else:
                error = VERROR

        return self.return_dict(title='Add Mod', error=error)

    @view_config(route_name='editmod', renderer='editmod.mak', permission='user')
    def editmod(self):
        error = ''
        post = self.request.params

        # Get mod
        mod = self.get_db_object(Mod)

        if 'btnSubmit' in post:
            params = get_params(post)
            if check_params(params):
                try:
                    for key in params:
                        mod[key] = params[key]
                    mod.save()
                    return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))
                except ValidationError:
                    error = VERROR
            else:
                error = VERROR
        return self.return_dict(title='Add Mod', error=error, v=mod)

    @view_config(route_name='modlist', renderer='modlist.mak')
    def modlist(self):
        post = self.request.params

        if 'btnSubmit' in post:
            mods = Mod.objects(Q(name__icontains=post['txtSearch']) | Q(author__icontains=post['txtSearch']))
        else:
            mods = Mod.objects

        return self.return_dict(title='Mod List', mods=mods)

    @view_config(route_name='flagmod', permission='user')
    def flagmod(self):
        mod = self.get_db_object(Mod, perm=False)
        mod.outdated = not mod.outdated
        mod.save()

        return HTTPFound(location=self.request.referrer)

    @view_config(route_name='deletemod', permission='user')
    def deletemod(self):
        # Get mod
        mod = self.get_db_object(Mod)

        if self.check_depends(mod):
            for version in mod.versions:
                version.mod_file.delete()
                version.delete()
            mod.delete()
            return self.success_url('modlist', mod.name + ' deleted successfully.')
        else:
            return HTTPFound(self.request.route_url('error', type='depends'))

    @view_config(route_name='viewmod', renderer='viewmod.mak')
    def viewmod(self):
        mod = self.get_db_object(Mod, perm=False)

        if self.logged_in is None:
            packs = []
        else:
            user = User.objects.get(username=self.logged_in)
            packs = Pack.objects(owner=user)

        return self.return_dict(title=mod.name, mod=mod, packs=packs, perm=self.has_perm(mod))


def get_params(post):
    return opt_dict(
        name=post.get('txtName'),
        author=post.get('txtAuthor'),
        install=post.get('txtInstall'),
        url=post.get('txtUrl'),
        target=post.get('selTarget'),
        permission=post.get('parPermission')
    )


def check_params(params):
    return re.match('^[\w ]+$', params['name']) and params['install'].isalnum()
