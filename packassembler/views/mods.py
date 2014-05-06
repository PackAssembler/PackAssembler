from pyramid.httpexceptions import HTTPFound
import packassembler.views.email as email
from ..form import ModForm, BannerForm
from pyramid.view import view_config
from ..schema import *
from .common import *


class ModViews(ViewBase):

    @view_config(route_name='modlist', renderer='modlist.mak', http_cache=3600)
    def modlist(self):
        post = self.request.params
        q = Q()

        if 'q' in post:
            q &= Q(name__icontains=post['q']) | Q(author__icontains=post['q'])

        if 'outdated' in post:
            q &= Q(outdated=True)

        if 'mc_version' in post:
            v = post['mc_version']
            if v in MCVERSIONS:
                versions = ModVersion.objects(Q(mc_min=v) | Q(mc_max=v))
                q &= Q(versions__in=versions)

        #mods = page_list(post, Mod.objects(q))
        mods = Mod.objects(q)
        return self.return_dict(
            title='Mods',
            mods=mods,
            packs=self.get_add_pack_data(),
            mc_versions=list(MCVERSIONS)
        )

    @view_config(route_name='qmlist', renderer='json')
    def qmlist(self):
        return {
            'baseUrl': self.request.route_url('modlist') + "/{}.json",
            'index': [{"uid": m.rid, "url": str(m.id)} for m in Mod.objects]
        }

    @view_config(route_name='adoptmod', permission='contributor')
    def adopt(self):
        # Get mod
        mod = self.get_db_object(Mod, perm=False)

        # Set owner to current user
        mod.owner = self.current_user
        mod.save()

        self.request.flash('Mod adopted.')
        return HTTPFound(self.request.route_url('viewmod', id=self.request.matchdict['id']))

    @view_config(route_name='disownmod', permission='user')
    def disown(self):
        # Get mod
        mod = self.get_db_object(Mod)

        mod.owner = None
        mod.save()

        self.request.flash('Mod disowned.')
        return HTTPFound(self.request.route_url('viewmod', id=self.request.matchdict['id']))

    @view_config(route_name='flagmod', permission='user')
    def flagmod(self):
        mod = self.get_db_object(Mod, perm=False)
        mod.outdated = not mod.outdated
        mod.save()

        if mod.outdated:
            self.send_out_of_date_notification(mod)

        return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))

    @view_config(route_name='flagmod', permission='user', renderer='json', xhr=True)
    def flagmod_ajax(self):
        mod = self.get_db_object(Mod, perm=False)

        js_out = {'success': True, 'outdated': not mod.outdated}
        mod.outdated = js_out['outdated']
        mod.save()

        if mod.outdated:
            self.send_out_of_date_notification(mod)

        return js_out

    @view_config(route_name='moveversion', permission='user')
    def moveversion(self):
        mod = self.get_db_object(Mod)

        ind = int(self.request.matchdict['index'])
        s = int(self.request.matchdict['shift'])

        mod.versions.insert(len(mod.versions) - ind - 1 + s, mod.versions.pop(-ind - 1))
        mod.save()

        return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))

    @view_config(route_name='quickmod', renderer='json')
    def quickmod(self):
        mod = self.get_db_object(Mod, perm=False)
        qm = {
            'name': mod.name,
            'author': {'developer': [mod.author]},
            'uid': mod.rid,
            'websiteUrl': mod.url,
            'updateUrl': self.request.url,
            'versions': []
        }
        if mod.description:
            qm['description'] = mod.description
        if mod.banner:
            qm['logoUrl'] = mod.banner.image
        for v in mod.versions:
            vdata = {
                'mcCompat': get_mcv_compat(v.mc_min, v.mc_max),
                'url': self.request.route_url('downloadversion', id=v.id) if v.mod_file else v.mod_file_url,
                'md5': v.md5,
                'name': v.version
            }
            if v.depends:
                vdata['references'] = [{'uid': dep.rid, 'type': 'depends'} for dep in v.depends]
            qm['versions'].append(vdata)

        return qm

    @view_config(route_name='editmodbanner', permission='user', renderer='genericform.mak')
    @view_config(route_name='editpackbanner', permission='user', renderer='genericform.mak')
    @view_config(route_name='editserverbanner', permission='user', renderer='genericform.mak')
    def editbanner(self):
        # Get our route name and post info
        rname = self.request.matched_route.name
        post = self.request.params

        # Get the object
        obj = self.get_db_object({
            'editmodbanner': Mod,
            'editpackbanner': Pack,
            'editserverbanner': Server
        }[rname], perm=False)

        banner = obj.banner or Banner()
        form = BannerForm(post, banner)

        prev = self.request.route_url(
            'view' + rname.replace('edit', '').replace('banner', ''),
            id=obj.id
        )

        if 'submit' in post and form.validate():
            form.populate_obj(banner)

            banner.text_color = banner.text_color.upper()

            # Don't save the banner if there is none to show
            if banner.image is None:
                obj.banner = None
            else:
                obj.banner = banner

            # Save the mod
            obj.save()

            return HTTPFound(location=prev)

        return self.return_dict(title='Edit Banner', f=form, cancel=prev)

    @view_config(route_name='addmod', renderer='genericform.mak', permission='contributor')
    def addmod(self):
        post = self.request.params
        form = ModForm(post)

        if 'submit' in post and form.validate():
            try:
                mod = Mod(owner=self.current_user)
                form.populate_obj(mod)
                mod.rid = slugify(form.name.data)
                mod.save()
                return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))
            except NotUniqueError:
                form.name.errors.append('Name or Readable ID Already Exists.')

        return self.return_dict(title='Add Mod', f=form, cancel=self.request.route_url('modlist'))

    @view_config(route_name='editmod', renderer='genericform.mak', permission='user')
    def editmod(self):
        mod = self.get_db_object(Mod)
        post = self.request.params
        form = ModForm(post, mod)

        if 'submit' in post and form.validate():
            form.populate_obj(mod)
            mod.save()

            self.request.flash('Changes saved.')
            return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))

        return self.return_dict(title='Edit Mod', f=form, cancel=self.request.route_url('viewmod', id=mod.id))

    @view_config(route_name='deletemod', permission='user')
    def deletemod(self):
        # Get mod
        mod = self.get_db_object(Mod)

        # Check if a PackBuild depends on a version
        no_version_deps = all([self.check_depends(i) for i in mod.versions])

        if self.check_depends(mod) and no_version_deps:
            for version in mod.versions:
                version.mod_file.delete()
            mod.delete()
            self.request.flash(mod.name + ' deleted successfully.')
            return HTTPFound(self.request.route_url('modlist'))
        else:
            self.request.flash_error('Could not delete the mod because a pack depends on it.')
            return HTTPFound(self.request.route_url('viewmod', id=mod.id))

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

    def send_out_of_date_notification(self, mod):
        url = self.request.route_url('viewmod', id=mod.id)
        email.mod_outdated(self.request.registry, mod.owner, mod.name, url)
