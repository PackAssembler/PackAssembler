from pyramid.httpexceptions import HTTPFound
from ..form import ModForm, BannerForm
from pyramid.view import view_config
from ..schema import *
from .common import *


class ModViews(ViewBase):

    @view_config(route_name='modlist', renderer='modlist.mak')
    def modlist(self):
        post = self.request.params

        mods = Mod.objects

        if 'q' in post:
            versions = ModVersion.objects(Q(mc_min=post['q']) | Q(mc_max=post['q']))

            if 'outdated' in post['q']:
                mods = mods(outdated=True)
                query = post['q'].replace('outdated', '').strip()
            else:
                query = post['q']

            mods = mods(
                Q(name__icontains=query) | Q(author__icontains=query) |
                Q(versions__in=versions))

        return self.return_dict(
            title='Mod List', mods=mods, packs=self.get_add_pack_data())

    @view_config(route_name='adoptmod', permission='contributor')
    def adopt(self):
        # Get mod
        mod = self.get_db_object(Mod, perm=False)

        # Set owner to current user
        mod.owner = self.current_user
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

    @view_config(route_name='flagmod', permission='user', renderer='json', xhr=True)
    def flagmod_ajax(self):
        mod = self.get_db_object(Mod, perm=False)

        js_out = {'success': True, 'outdated': not mod.outdated}
        mod.outdated = js_out['outdated']
        mod.save()

        return js_out

    @view_config(route_name='editbanner', permission='user', renderer='genericform.mak')
    def editbanner(self):
        post = self.request.params
        mod = self.get_db_object(Mod, perm=False)
        banner = mod.banner or Banner()
        form = BannerForm(post, banner)

        if 'submit' in post and form.validate():
            form.populate_obj(banner)

            banner.text_color = banner.text_color.upper()

            # Don't save the banner if there is none to show
            if banner.image is None:
                mod.banner = None
            else:
                mod.banner = banner

            # Save the mod
            mod.save()

            return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))

        return self.return_dict(title='Edit Banner', f=form, cancel=self.request.route_url('viewmod', id=mod.id))

    @view_config(route_name='addmod', renderer='genericform.mak', permission='contributor')
    def addmod(self):
        post = self.request.params
        form = ModForm(post)

        if 'submit' in post and form.validate():
            mod = Mod(owner=self.current_user)
            form.populate_obj(mod)
            mod.rid = form.name.data.replace(' ', '_')
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
            mod.delete()
            return self.success_url('modlist', mod.name + ' deleted successfully.')
        else:
            return HTTPFound(self.request.route_url('error', type='depends'))

    @view_config(route_name='viewmod', renderer='viewmod.mak')
    def viewmod(self):
        mod = self.get_db_object(Mod, perm=False)

        return self.return_dict(title=mod.name,
                                mod=mod,
                                packs=self.get_add_pack_data(),
                                perm=self.has_perm(mod),
                                by_author=Mod.objects(
                                    author__icontains=mod.author),
                                with_mod=Pack.objects(mods=mod)
                                )
