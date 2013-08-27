from pyramid.httpexceptions import HTTPFound
from ..form import PackForm, PackModForm
from pyramid.response import Response
from pyramid.view import view_config
from ..schema import *
from .common import *
import re


class MMLServerPack(MMLServerView):
    @view_config(route_name='addpack', renderer='genericform.mak', permission='user')
    def addpack(self):
        error = ''
        post = self.request.params
        form = PackForm(post)

        if 'submit' in post and form.validate():
            try:
                pack = Pack(owner=User.objects.get(username=self.logged_in), name=form.name.data).save()
                return HTTPFound(location=self.request.route_url('viewpack', id=pack.id))
            except NotUniqueError:
                form.name.errors.append('Already exists.')

        return self.return_dict(title="Add Pack", f=form, cancel=self.request.route_url('modlist'))

    @view_config(route_name='clonepack', permission='user')
    def clonepack(self):
        current_pack = self.get_db_object(Pack, perm=False)
        try:
            new_pack = Pack(
                owner=User.objects.get(username=self.logged_in),
                name='[{0}] {1}'.format(self.logged_in, current_pack.name),
                mods=current_pack.mods).save()
        except NotUniqueError:
            return HTTPFound(location=self.request.route_url('error', type='already_cloned'))
        return HTTPFound(location=self.request.route_url('viewpack', id=new_pack.id))

    @view_config(route_name='editpack', renderer='genericform.mak', permission='user')
    def editpack(self):
        pack = self.get_db_object(Pack)
        post = self.request.params
        form = PackForm(post, pack)

        if 'submit' in post and form.validate():
            pack.name = form.name.data
            try:
                pack.save()
                return HTTPFound(location=self.request.route_url('viewpack', id=pack.id))
            except NotUniqueError:
                form.name.errors.append('Already exists.')

        return self.return_dict(title="Edit Pack", f=form, cancel=self.request.route_url('viewpack', id=pack.id))

    @view_config(route_name='packlist', renderer='packlist.mak')
    def packlist(self):
        post = self.request.params

        if 'q' in post:
            packs = Pack.objects(name__icontains=post['q'])
        else:
            packs = Pack.objects

        return self.return_dict(title="Pack List", packs=packs)

    @view_config(route_name='deletepack', permission='user')
    def deletepack(self):
        # Get pack
        pack = self.get_db_object(Pack)

        if self.check_depends(pack):
            pack.delete()
            return self.success_url('packlist', pack.name + ' deleted successfully.')
        else:
            return HTTPFound(self.request.route_url('error', type='depends'))

    @view_config(route_name='viewpack', renderer='viewpack.mak')
    def viewpack(self):
        pack = self.get_db_object(Pack, perm=False)

        return self.return_dict(title=pack.name, pack=pack, perm=self.has_perm(pack))

    @view_config(route_name='packjson')
    def packjson(self):
        pack = self.get_db_object(Pack, perm=False)

        return Response(pack.to_json(), content_type='application/json')

    @view_config(route_name='addpackmod', renderer='genericform.mak', permission='user')
    def addpackmod(self):
        post = self.request.params
        form = PackModForm(post)

        if self.has_perm(Pack.objects(id=self.request.matchdict['id']).only('owner').first()):
            if 'id' in post and form.validate():
                try:
                    Pack.objects(id=self.request.matchdict['id']).update_one(add_to_set__mods=post['id'])
                    return HTTPFound(self.request.route_url('viewpack', id=self.request.matchdict['id']))
                except DoesNotExist:
                    form.id.errors.append('Mod does not exist.')
            elif 'mods' in post:
                Pack.objects(id=self.request.matchdict['id']).update_one(add_to_set__mods=post.getall('mods'))
                return HTTPFound(self.request.route_url('viewpack', id=self.request.matchdict['id']))
        else:
            return HTTPForbidden()
        return self.return_dict(title="Add Mod to Pack", f=form, cancel=self.request.route_url('viewpack', id=self.request.matchdict['id']))

    @view_config(route_name='removepackmod', permission='user')
    def removepackmod(self):
        if self.has_perm(Pack.objects(id=self.request.matchdict['packid']).only('owner').first()):
            Pack.objects(id=self.request.matchdict['packid']).update_one(pull__mods=self.request.matchdict['modid'])
        else:
            return HTTPForbidden()
        return HTTPFound(self.request.referer)
