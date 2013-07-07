from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden, HTTPBadRequest
from pyramid.view import view_config
from pyramid.response import Response
from .common import MMLServerView, VERROR
from ..schema import *
from json import dumps
from bson import json_util


class MMLServerPackBuild(MMLServerView):
    def linkerror(self, mod, message):
        return '<a href="' + self.request.route_url('viewmod', modid=mod.id) + '">' + mod.name + '</a>' + ' ' + message

    @view_config(route_name='addbuild', renderer='editbuild.mak', permission='user')
    def addbuild(self):
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
            if 'selMCVersion' in post and 'txtForgeVersion' in post and 'txtConfig' in post \
               and post['selMCVersion'] and post['txtForgeVersion']:
                elist = []
                splitm = post['selMCVersion'].split('.')
                jdict = {
                    'pack_id': pack.id,
                    'pack_name': pack.name,
                    'config': post['txtConfig'],
                    'mc_version': post['selMCVersion'],
                    'forge_version': post['txtForgeVersion'],
                    'mods': {}
                }
                for mod in pack.mods:
                    mc_compat = [i for i in mod.versions 
                                 if i.mc_min.split('.') <= splitm 
                                 and i.mc_max.split('.') >= splitm]
                    if mc_compat:
                        forge_compat = []
                        for version in mc_compat:
                            dversion = version.to_mongo()
                            forge_min = dversion.get('forge_min', '0.0.0.000').split('.')
                            forge_max = dversion.get('forge_max', '9.9.9.999').split('.')
                            splitf = post['txtForgeVersion'].split('.')
                            if forge_min <= splitf and forge_max >= splitf:
                                forge_compat.append(version)
                        if forge_compat:
                            selected = max(forge_compat, key=lambda v: v.version.split('.'))
                            jdict['mods'][str(mod.id)] = [selected.id, mod.install]
                        else:
                            elist.append(self.linkerror(mod, 'is incompatible with Forge ' + post['txtForgeVersion']))
                    else:
                        elist.append(self.linkerror(mod, 'is incompatible with Minecraft ' + post['selMCVersion']))
                if elist:
                    error = '<ul>'
                    for e in elist:
                        error += '<li>' + e + '</li>'
                    error += '</ul>'
                else:
                    pb = PackBuild(build=dumps(jdict, default=json_util.default), mc_version=post['selMCVersion'],
                        forge_version=post['txtForgeVersion'], pack=pack, revision=pack.latest+1)
                    if post['txtConfig']:
                        pb.config = post['txtConfig']
                    pb.save()
                    pack.latest = pb.revision
                    pack.builds.append(pb)
                    pack.save()
                    return HTTPFound(self.request.route_url('viewpack', packid=pack.id))
            else:
                error = VERROR
        return self.return_dict(title='New Build', error=error)

    @view_config(route_name='removebuild', permission='user')
    def removebuild(self):
        try:
            pb = PackBuild.objects.get(id=self.request.matchdict['buildid'])
        except DoesNotExist:
            return HTTPNotFound()
        if not self.has_perm(pb.pack):
            return HTTPForbidden()

        pb.delete()
        return HTTPFound(location=self.request.referer)

    @view_config(route_name='getbuild')
    def getbuild(self):
        try:
            pb = PackBuild.objects.get(id=self.request.matchdict['buildid'])
        except DoesNotExist:
            return HTTPNotFound()
        return Response(pb.build)
