from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from ..schema import *
from .common import *


class MMLServerServers(MMLServerView):
    @view_config(route_name='addserver', renderer='editserver.mak', permission='user')
    def addserver(self):
        error = ''
        post = self.request.params

        if 'btnSubmit' in post:
            params = opt_dict(
                name=post['txtName'],
                url=post['txtUrl'],
                host=post['txtHost'],
                port=post['txtPort'],
                config=post['txtConfig']
            )
            try:
                pack = Pack.objects.get(id=post['txtPackID'])
                pb = PackBuild.objects.get(revision=post['txtRevision'], pack=pack)
                params['build'] = pb
                params['owner'] = User.objects.get(username=self.logged_in)
                server = Server(**params).save()
                return HTTPFound(location=self.request.route_url('viewserver', id=server.id))
            except DoesNotExist:
                error = 'Pack or Revision Does Not Exist'
            except ValidationError:
                error = VERROR
        return self.return_dict(title='Add Server', error=error)

    @view_config(route_name='editserver', permission='user', renderer='editserver.mak')
    def editserver(self):
        error = ''
        post = self.request.params

        # Get current data
        server = self.get_db_object(Server)

        if 'btnSubmit' in post:
            params = opt_dict(
                name=post['txtName'],
                url=post['txtUrl'],
                host=post['txtHost'],
                port=post['txtPort'],
                config=post['txtConfig']
            )
            try:
                pack = Pack.objects.get(id=post['txtPackID'])
                pb = PackBuild.objects.get(revision=post['txtRevision'], pack=pack)
                params['build'] = pb
                for key in params:
                    if server[key] != params[key]:
                        server[key] = params[key]
                server.save()
                return HTTPFound(location=self.request.route_url('viewserver', id=server.id))
            except DoesNotExist:
                error = 'Pack or Revision Does Not Exist'
            except ValidationError:
                error = VERROR
        return self.return_dict(title='Edit Server', error=error, v=server)

    @view_config(route_name='serverlist', renderer='serverlist.mak')
    def serverlist(self):
        post = self.request.params

        if 'btnSubmit' in post:
            servers = Server.objects(name__icontains=post['txtSearch'])
        else:
            servers = Server.objects

        return self.return_dict(title="Server List", servers=servers)

    @view_config(route_name='deleteserver', permission='user')
    def deleteserver(self):
        server = self.get_db_object(Server)

        server.delete()
        return HTTPFound(location=self.request.route_url('serverlist'))

    @view_config(route_name='viewserver', renderer='viewserver.mak')
    def viewserver(self):
        server = self.get_db_object(Server, perm=False)

        return self.return_dict(title=server.name, server=server, perm=self.has_perm(server))

    @view_config(route_name='serverjson')
    def serverjson(self):
        server = self.get_db_object(Server, perm=False)

        return Response(server.to_json(), content_type='application/json')
