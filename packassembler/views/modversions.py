from ..form import ModVersionForm, EditModVersionForm, QuickModVersionForm
from pyramid.response import Response, FileIter
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from ..security import check_pass
from ..schema import *
from .common import *
import requests


class VersionViews(ViewBase):

    @view_config(route_name='addversion', renderer='editmodversion.mak',
                 permission='user')
    def addversion(self):
        mod = self.get_db_object(Mod)
        post = self.request.params
        form = ModVersionForm(post)

        if 'submit' in post and form.validate() and not version_exists(mod, form.version.data):
            mv = ModVersion(mod=mod)
            form.populate_obj(mv)
            try:
                mv.mod_file = post[form.mod_file.name].file
                mv.mod_file_url = None
            except AttributeError:
                if form.upload_from_url.data:
                    mv.mod_file = requests.get(form.mod_file_url.data).content
                    mv.mod_file_url = None
                else:
                    mv.mod_file_url_md5, mv.mod_file_url = url_md5(form.mod_file_url.data)

            mv.depends = get_depends(post)
            mv.save()

            mod.versions.append(mv)
            mod.outdated = False
            mod.save()
            return HTTPFound(location=self.request.route_url('viewmod', id=mod.id))

        mv = (mod.versions[-1] if mod.versions else None)
        return self.return_dict(
            title="Add Mod Version", mods=Mod.objects(id__ne=mod.id), mv=mv,
            f=form, cancel=self.request.route_url('viewmod', id=mod.id)
        )

    @view_config(route_name='quickadd')
    def quickadd(self):
        post = self.request.params
        mod = self.get_db_object(Mod, perm=False)

        user = check_pass(post['username'], post['password'])
        if not user or mod.owner != user:
            raise NoPermission

        form = QuickModVersionForm(post)

        if form.validate():
            mv = ModVersion(mod=mod)
            mv.mc_min = form.mc.data
            mv.mc_max = form.mc.data
            mv.version = form.version.data
            mv.mod_file = requests.get(form.url.data).content
            mv.depends = mod.versions[-1].depends if mod.versions else []
            mv.devel = True
            mv.save()

            mod.versions.append(mv)
            mod.outdated = False
            mod.save()
            return Response("All good!")

        return Response("Something went wrong...")

    @view_config(route_name='editversion', renderer='editmodversion.mak', permission='user')
    def editversion(self):
        mv = self.get_db_object(ModVersion)
        post = self.request.params
        form = EditModVersionForm(post, mv)

        if 'submit' in post and form.validate():
            if form.version.data == mv.version or not version_exists(mv.mod, form.version.data):
                form.populate_obj(mv)
                try:
                    mv.mod_file = post[form.mod_file.name].file
                    mv.mod_file_url = None
                    mv.mod_file_url_md5 = None
                except AttributeError:
                    if mv.mod_file_url:
                        if form.upload_from_url.data:
                            mv.mod_file = requests.get(form.mod_file_url.data).content
                            mv.mod_file_url = None
                        else:
                            mv.mod_file_url_md5, mv.mod_file_url = url_md5(form.mod_file_url.data)
                            mv.mod_file = None

                mv.depends = get_depends(post)
                mv.save()

                return HTTPFound(location=self.request.route_url('viewmod', id=mv.mod.id))

        return self.return_dict(
            title="Edit Mod Version", mods=Mod.objects, mv=mv,
            f=form, cancel=self.request.route_url('viewmod', id=mv.mod.id)
        )

    @view_config(route_name='downloadversion')
    def downloadversion(self):
        # Get modversion
        mv = self.get_db_object(ModVersion, perm=False)

        cdisp = 'attachment; filename="{0}-{1}.jar"'.format(mv.mod.name, mv.version)
        if mv.mod_file:
            return Response(app_iter=FileIter(mv.mod_file), content_type='application/zip', content_disposition=cdisp)
        else:
            return HTTPFound(mv.mod_file_url)

    @view_config(route_name='deleteversion', permission='user')
    def deleteversion(self):
        # Get modversion
        mv = self.get_db_object(ModVersion)

        if self.check_depends(mv):
            if mv.mod_file:
                mv.mod_file.delete()
            mv.delete()
            return HTTPFound(location=self.request.route_url('viewmod', id=mv.mod.id))
        else:
            return HTTPFound(self.request.route_url('error', type='depends'))

    @view_config(route_name='versiondetails', renderer='versiondetails.mak')
    def versiondetails(self):
        return {'version': self.get_db_object(ModVersion, perm=False)}


def get_depends(post):
    req = []
    for mid in post.getall('depends'):
        try:
            req.append(Mod.objects.get(id=mid))
        except DoesNotExist:
            pass

    return req if req else None


def version_exists(m, version):
    return any(x.version == version for x in m.versions)
