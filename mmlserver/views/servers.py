from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from .common import MMLServerView, opt_dict
from pyramid.view import view_config
from ..schema import *
import re

class MMLServerServers(MMLServerView):
    @view_config(route_name='addserver', permission='user', renderer='editserver.mak')
    def addserver(self):
        error = ''
        post = self.request.params
        if 'btnSubmit' in post:
            params = opt_dict(
                name=post['txtName'],
                url=post['txtUrl']
            )
            try:
                pack = Pack.objects.get(id=post['txtPackID'])
                pb = PackBuild.objects.get(revision=post['txtRevision'], pack=pack)
                params['build'] = pb
                params['owner'] = User.objects.get(username=self.logged_in)
                server = Server(**params).save()
                return HTTPFound(location=self.request.route_url('viewserver', serverid=server.id))
            except DoesNotExist:
                error = 'Pack or Revision Does Not Exist'
            except MultipleObjectsReturned:
                error = 'Something is Extremely Wrong with the Pack'
        return self.return_dict(title='Add Server', error=error)

    @view_config(route_name='editserver', permission='user', renderer='editserver.mak')
    def editserver(self):
        error = ''
        post = self.request.params
        # Get current data
        try:
            server = Server.objects.get(id=self.request.matchdict['serverid'])
        except DoesNotExist:
            return HTTPNotFound()
        # Check permission
        if not self.has_perm(server):
            return HTTPForbidden()
        if 'btnSubmit' in post:
            params = opt_dict(
                name=post['txtName'],
                url=post['txtUrl']
            )
            try:
                pack = Pack.objects.get(id=post['txtPackID'])
                pb = PackBuild.objects.get(revision=post['txtRevision'], pack=pack)
                params['build'] = pb
                for key in params:
                    if server[key] != params[key]:
                        server[key] = params[key]
                server.save()
                return HTTPFound(location=self.request.route_url('viewserver', serverid=server.id))
            except DoesNotExist:
                error = 'Pack or Revision Does Not Exist'
            except MultipleObjectsReturned:
                error = 'Something is Extremely Wrong with the Pack'
        return self.return_dict(title='Edit Server', error=error, v=server)

    @view_config(route_name='serverlist', renderer='serverlist.mak')
    def serverlist(self):
        return self.return_dict(title="Server List", servers=Server.objects)

    @view_config(route_name='deleteserver', permission='user')
    def deleteserver(self):
        try:
            server = Server.objects.get(id=self.request.matchdict['serverid'])
        except DoesNotExist:
            return HTTPNotFound()
        # Check permission
        if not self.has_perm(server):
            return HTTPForbidden()
        server.delete()
        return HTTPFound(location=self.request.route_url('home'))

    @view_config(route_name='viewserver', renderer='viewserver.mak')
    def viewserver(self):
        try:
            server = Server.objects.get(id=self.request.matchdict['serverid'])
        except DoesNotExist:
            return HTTPNotFound()
        return self.return_dict(title=server.name, server=server, perm=self.has_perm(server))
