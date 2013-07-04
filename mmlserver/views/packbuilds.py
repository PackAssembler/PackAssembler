from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.view import view_config
from .common import MMLServerView
from ..schema import *


class MMLServerPackBuild(MMLServerView):
    @view_config(route_name='addbuild', renderer='editbuild.mak', permission='user')
    def addbuild(self):
        # Defaults
        error = ''
        # Get post data
        post = self.request.params
        # Get pack to make build of
        try:
            pack = Pack.objects.get(id=self.request.matchdict['packid'])
        except DoesNotExist:
            return HTTPNotFound()
        # Check permission
        if not self.has_perm(pack):
            return HTTPForbidden()
        if 'btnSubmit' in post:
            print('Yes')
            print(post)
            if 'selMCVersion' in post and 'txtForgeVersion' in post:
                print('Yes')
                splitm = post['selMCVersion'].split('.')
                for mod in pack.mods:
                    mc_compat = [i for i in mod.versions if i.mc_min.split('.') <= splitm and i.mc_max.split('.') >= splitm]
                    if mc_compat:
                        forge_compat = []
                        for version in mc_compat:
                            forge_min = version.get('forge_min', '0.0.0.000').split('.')
                            forge_max = version.get('forge_max', '9.9.9.999').split('.')
                            splitf = post['txtForgeVersion'].split('.')
                            if forge_min <= splitf and forge_max >= splitf:
                                forge_compat.append(version)
                        if forge_compat:
                            print(forge_compat)
                        else:
                            error += mod.name + 'is incompatible with Forge ' + post['txtForgeVersion']
                    else:
                        error += mod.name + 'is incompatible with Minecraft ' + post['selMCVersion']
        return self.return_dict(title='New Build', error=error)
