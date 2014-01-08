from pyramid.httpexceptions import HTTPFound
from .packbuilds import generate_mcu_xml
from pyramid.response import Response
from pyramid.view import view_config
from ..form import ServerForm
from ..schema import *
from .common import *


class ServerViews(ViewBase):

    @view_config(route_name='addserver', renderer='genericform.mak', permission='user')
    def addserver(self):
        error = ''
        post = self.request.params
        form = ServerForm(post, port=25565)

        if 'submit' in post and form.validate():
            try:
                if form.packid.data:
                    pack = Pack.objects.get(id=form.packid.data)
                    pb = PackBuild.objects.get(
                        revision=form.revision.data,
                        pack=pack)
                else:
                    pb = None

                params = opt_dict(
                    name=form.name.data,
                    rid=slugify(form.name.data),
                    url=form.url.data,
                    host=form.host.data,
                    port=form.port.data,
                    config=form.config.data,
                    build=pb,
                    owner=self.current_user
                )
                server = Server(**params).save()
                return HTTPFound(location=self.request.route_url('viewserver', id=server.id))
            except DoesNotExist:
                error = 'Pack or Revision Does Not Exist'
            except NotUniqueError:
                form.name.errors.append('Name or Readable ID Already Exists.')

        return self.return_dict(title='Add Server', error=error, f=form, cancel=self.request.route_url('serverlist'))

    @view_config(route_name='editserver', permission='user', renderer='genericform.mak')
    def editserver(self):
        error = ''
        server = self.get_db_object(Server)
        post = self.request.params
        form = ServerForm(
            post,
            server,
            packid=server.build.pack.id if server.build else "",
            revision=server.build.revision if server.build else "")

        if 'submit' in post and form.validate():
            try:
                if form.packid.data:
                    pack = Pack.objects.get(id=form.packid.data)
                    pb = PackBuild.objects.get(
                        revision=form.revision.data,
                        pack=pack)
                else:
                    pb = None

                params = opt_dict(
                    name=form.name.data,
                    url=form.url.data,
                    host=form.host.data,
                    port=form.port.data,
                    config=form.config.data,
                    build=pb
                )
                for key, val in params.items():
                    server[key] = val
                server.save()
                return HTTPFound(location=self.request.route_url('viewserver', id=server.id))
            except DoesNotExist:
                error = 'Pack or Revision Does Not Exist'

        return self.return_dict(title='Edit Server', error=error, f=form, cancel=self.request.route_url('viewserver', id=server.id))

    @view_config(route_name='serverlist', renderer='serverlist.mak')
    def serverlist(self):
        post = self.request.params

        if 'q' in post:
            servers = Server.objects(name__icontains=post['q'])
        else:
            servers = Server.objects

        return self.return_dict(title="Servers", servers=servers)

    @view_config(route_name='deleteserver', permission='user')
    def deleteserver(self):
        server = self.get_db_object(Server)

        server.delete()
        return HTTPFound(location=self.request.route_url('serverlist'))

    @view_config(route_name='viewserver', renderer='viewserver.mak')
    def viewserver(self):
        server = self.get_db_object(Server, perm=False)

        return self.return_dict(title=server.name, server=server, perm=self.has_perm(server))

    @view_config(route_name='viewserver', request_method='GET', accept='application/json', xhr=True)
    def viewserver_json(self):
        server = self.get_db_object(Server, perm=False)

        return Response(server.to_json(), content_type='application/json')

    @view_config(route_name='mcuxmlserver')
    def mcuxmlserver(self):
        server = self.get_db_object(Server, perm=False)
        if server.build:
            return Response(generate_mcu_xml(self.request, server.build, server=server), content_type='application/xml')
        else:
            return Response("Could not complete your request. Server does not have a build associated with it.", content_type='text/plain')
