from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from ..form import PackForm
from ..schema import *
from .common import *


class PackViews(ViewBase):

    @view_config(route_name='addpack', renderer='genericform.mak', permission='user')
    def addpack(self):
        post = self.request.params
        form = PackForm(post)

        if 'submit' in post and form.validate():
            try:
                pack = Pack(
                    owner=self.current_user,
                    name=form.name.data,
                    devel=form.devel.data,
                    rid=slugify(form.name.data)
                ).save()
                return HTTPFound(location=self.request.route_url('viewpack', id=pack.id))
            except NotUniqueError:
                form.name.errors.append('Name or Readable ID Already Exists.')

        return self.return_dict(title="Add Pack", f=form, cancel=self.request.route_url('modlist'))

    @view_config(route_name='clonepack', permission='user')
    def clonepack(self):
        current_pack = self.get_db_object(Pack, perm=False)
        try:
            new_pack = Pack(
                owner=self.current_user,
                name='[{0}] {1}'.format(self.logged_in, current_pack.name),
                devel=current_pack.devel,
                mods=current_pack.mods,
                rid=self.logged_in + '-' + current_pack.rid).save()
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
            pack.devel = form.devel.data
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

        return self.return_dict(title="Packs", packs=packs)

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

        return self.return_dict(
            title=pack.name, pack=pack,
            perm=self.has_perm(pack),
            packs=self.get_add_pack_data()
        )

    @view_config(route_name='viewpack', request_method='GET', accept='application/json', xhr=True)
    def viewpack_json(self):
        print(self.request.accept)
        pack = self.get_db_object(Pack, perm=False)

        return Response(pack.to_json(), content_type='application/json')

    @view_config(route_name='mcuxmlpack')
    def mcuxmlpack(self):
        pack = self.get_db_object(Pack, perm=False)

        if pack.builds:
            return HTTPFound(self.request.route_url('mcuxml', id=pack.builds[-1].id))
        else:
            return Response('No builds available.')

    @view_config(route_name='addpackmod', renderer='genericform.mak', permission='user')
    def addpackmod(self):
        post = self.request.params

        if self.has_perm(Pack.objects(id=self.request.matchdict['id']).only('owner').first()):
            Pack.objects(id=self.request.matchdict['id']).update_one(
                add_to_set__mods=post.getall('mods'))
            return HTTPFound(self.request.route_url('viewpack', id=self.request.matchdict['id']))
        else:
            return HTTPForbidden()

    @view_config(route_name='removepackmod', permission='user')
    def removepackmod(self):
        if self.has_perm(Pack.objects(id=self.request.matchdict['packid']).only('owner').first()):
            Pack.objects(id=self.request.matchdict['packid']).update_one(
                pull__mods=self.request.matchdict['modid'])
            return HTTPFound(self.request.route_url('viewpack', id=self.request.matchdict['packid']))
        else:
            return HTTPForbidden()
