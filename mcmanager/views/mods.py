from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from ..form import ModForm
from ..schema import *
from .common import *
import re


class MMLServerMod(MMLServerView):
    @view_config(route_name='modlist', renderer='modlist.mak')
    def modlist(self):
        post = self.request.params

        if 'q' in post:
            mods = Mod.objects(Q(name__icontains=post['q']) | Q(author__icontains=post['q']))
        else:
            mods = Mod.objects

        return self.return_dict(title='Mod List', mods=mods)

    @view_config(route_name='adoptmod', permission='trusted')
    def adopt(self):
        # Get mod
        mod = self.get_db_object(Mod, perm=False)

        # Set owner to current user
        mod.owner = User.objects.get(username=self.logged_in)
        mod.save()

        return HTTPFound(self.request.route_url('viewmod', id=self.request.matchdict['id']))

    @view_config(route_name='disownmod', permission='user')
    def disown(self):
        # Get mod
        mod = self.get_db_object(Mod)

        # Set owner to orphan
        mod.owner = self.get_orphan_user()
        mod.save()

        return HTTPFound(self.request.route_url('viewmod', id=self.request.matchdict['id']))

    @view_config(route_name='flagmod', permission='user')
    def flagmod(self):
        mod = self.get_db_object(Mod, perm=False)
        mod.outdated = not mod.outdated
        mod.save()

        return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))

    @view_config(route_name='addmod', renderer='genericform.mak', permission='trusted')
    def addmod(self):
        post = self.request.params
        form = ModForm(post, install='mods')

        if 'submit' in post and form.validate():
            mod = Mod(owner=User.objects.get(username=self.logged_in))
            form.populate_obj(mod)
            mod.save()
            return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))

        return self.return_dict(title='Add Mod', f=form, cancel=self.request.route_url('modlist'))

    @view_config(route_name='editmod', renderer='genericform.mak', permission='user')
    def editmod(self):
        mod = self.get_db_object(Mod)
        post = self.request.params
        form = ModForm(post, mod)

        if 'submit' in post and form.validate():
            form.populate_obj(mod)
            mod.save()
            return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))

        return self.return_dict(title='Edit Mod', f=form, cancel=self.request.route_url('viewmod', id=mod.id))

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
