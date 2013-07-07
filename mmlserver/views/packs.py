from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
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
                        return HTTPFound(location=self.request.route_url('viewpack', packid=pack.id))
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
        try:
            pack = Pack.objects.get(id=self.request.matchdict['packid'])
        except DoesNotExist:
            return HTTPNotFound()
        if not self.has_perm(pack):
            return HTTPForbidden()

        if 'btnSubmit' in post:
            params = opt_dict(name=post.get('txtName'))
            if 'name' in params:
                if re.match('^[\w ]+$', params['name']):
                    try:
                        for key in params:
                            if pack[key] != params[key]:
                                pack[key] = params[key]
                        pack.save()
                        return HTTPFound(location=self.request.route_url('viewpack', packid=pack.id))
                    except ValidationError:
                        error = VERROR
                else:
                    error = VERROR
        return self.return_dict(title="Edit Pack", error=error, v=pack)

    @view_config(route_name='packlist', renderer='packlist.mak')
    def packlist(self):
        return self.return_dict(title="Pack List", packs=Pack.objects)

    @view_config(route_name='deletepack', permission='user')
    def deletepack(self):
        # Get pack
        try:
            pack = Pack.objects.get(id=self.request.matchdict['packid'])
        except DoesNotExist:
            return HTTPNotFound()
        if not self.has_perm(pack):
            return HTTPForbidden()

        pack.delete()
        return self.success_url('packlist', pack.name + ' deleted successfully.')

    @view_config(route_name='viewpack', renderer='viewpack.mak')
    def viewpack(self):
        try:
            pack = Pack.objects.get(id=self.request.matchdict['packid'])
        except DoesNotExist:
            return HTTPNotFound()
        else:
            return self.return_dict(title=pack.name, pack=pack, perm=self.has_perm(pack))

    @view_config(route_name='addpackmod', renderer='addpackmod.mak', permission='user')
    def addpackmod(self):
        error = ''
        post = self.request.params
        if self.has_perm(Pack.objects(id=self.request.matchdict['packid']).only('owner').first()):
            if 'btnSubmit' in post:
                Pack.objects(id=self.request.matchdict['packid']).update_one(push__mods=Mod.objects.get(id=post['txtModID']))
                return HTTPFound(self.request.route_url('viewpack', packid=self.request.matchdict['packid']))
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
