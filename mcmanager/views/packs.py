from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from ..schema import *
from .common import *
import re


class MMLServerPack(MMLServerView):
    @view_config(route_name='addpack', renderer='editpack.mak', permission='user')
    def addpack(self):
        error = ''
        post = self.request.params

        if 'btnSubmit' in post:
            params = opt_dict(name=post.get('txtName'))
            if 'name' in params:
                if re.match('^[\w ]+$', params['name']):
                    try:
                        pack = Pack(owner=User.objects.get(username=self.logged_in), **params).save()
                        return HTTPFound(location=self.request.route_url('viewpack', id=pack.id))
                    except ValidationError:
                        error = VERROR
                else:
                    error = VERROR
        return self.return_dict(title="Add Pack", error=error)

    @view_config(route_name='editpack', renderer='editpack.mak', permission='user')
    def editpack(self):
        error = ''
        post = self.request.params

        # Get pack
        pack = self.get_db_object(Pack)

        if 'btnSubmit' in post:
            params = opt_dict(name=post.get('txtName'))
            if 'name' in params:
                if re.match('^[\w ]+$', params['name']):
                    try:
                        for key in params:
                            if pack[key] != params[key]:
                                pack[key] = params[key]
                        pack.save()
                        return HTTPFound(location=self.request.route_url('viewpack', id=pack.id))
                    except ValidationError:
                        error = VERROR
                else:
                    error = VERROR
        return self.return_dict(title="Edit Pack", error=error, v=pack)

    @view_config(route_name='packlist', renderer='packlist.mak')
    def packlist(self):
        post = self.request.params

        if 'btnSubmit' in post:
            packs = Pack.objects(name__icontains=post['txtSearch'])
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

    @view_config(route_name='addpackmod', renderer='addpackmod.mak', permission='user')
    def addpackmod(self):
        error = ''
        post = self.request.params
        if self.has_perm(Pack.objects(id=self.request.matchdict['id']).only('owner').first()):
            if 'btnSubmit' in post:
                try:
                    Pack.objects(id=self.request.matchdict['id']).update_one(add_to_set__mods=Mod.objects.get(id=post['txtModID']))
                    return HTTPFound(self.request.route_url('viewpack', id=self.request.matchdict['id']))
                except DoesNotExist:
                    error = 'Mod Does not Exist.'
        else:
            return HTTPForbidden()
        return self.return_dict(title="Add Mod to Pack", error=error)

    @view_config(route_name='removepackmod', permission='user')
    def removepackmod(self):
        if self.has_perm(Pack.objects(id=self.request.matchdict['packid']).only('owner').first()):
            Pack.objects(id=self.request.matchdict['packid']).update_one(pull__mods=Mod.objects.get(id=self.request.matchdict['modid']))
        else:
            return HTTPForbidden()
        return HTTPFound(self.request.referer)
