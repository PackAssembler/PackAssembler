from pyramid.httpexceptions import HTTPFound
from .common import MMLServerView, VERROR
from pyramid.response import Response
from pyramid.view import view_config
from ..form import PackBuildForm
from bson import json_util
from json import dumps
from ..schema import *


class MMLServerPackBuild(MMLServerView):
    def linkerror(self, mod, message):
        return '<a href="' + self.request.route_url('viewmod', id=mod.id) + '">' + mod.name + '</a>' + ' ' + message

    @view_config(route_name='addbuild', renderer='genericform.mak', permission='user')
    def addbuild(self):
        error = ''
        pack = self.get_db_object(Pack)
        post = self.request.params
        form = PackBuildForm(post)

        if 'submit' in post and form.validate():
            elist = []

            splitm = form.mc_version.data.split('.')
            splitf = form.forge_version.data.split('.')

            jdict = {
                'pack_id': pack.id,
                'pack_name': pack.name,
                'config': form.config.data,
                'mc_version': form.mc_version.data,
                'forge_version': form.forge_version.data,
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
                        if forge_min <= splitf and forge_max >= splitf:
                            forge_compat.append(version)
                    if forge_compat:
                        selected = max(forge_compat, key=lambda v: v.version.split('.'))
                        jdict['mods'][str(mod.id)] = {
                            'install': mod.install,
                            'target': mod.target,
                            'version': selected.id
                        }
                    else:
                        elist.append(self.linkerror(mod, 'is incompatible with Forge ' + form.forge_version.data))
                else:
                    elist.append(self.linkerror(mod, 'is incompatible with Minecraft ' + form.mc_version.data))
            if elist:
                error = '<ul>'
                for e in elist:
                    error += '<li>' + e + '</li>'
                error += '</ul>'
            else:
                pb = PackBuild(build=dumps(jdict, default=json_util.default), mc_version=form.mc_version.data,
                               forge_version=form.forge_version.data, pack=pack, revision=pack.latest+1)
                if form.config.data:
                    pb.config = form.config.data
                pb.save()
                pack.latest = pb.revision
                pack.builds.append(pb)
                pack.save()
                return HTTPFound(self.request.route_url('viewpack', id=pack.id))

        return self.return_dict(title='New Build', error=error, f=form, cancel=self.request.route_url('viewpack', id=pack.id))

    @view_config(route_name='removebuild', permission='user')
    def removebuild(self):
        pb = self.get_db_object(PackBuild)

        if self.check_depends(pb):
            pb.delete()
            return HTTPFound(location=self.request.referer)
        else:
            return HTTPFound(self.request.route_url('error', type='depends'))

    @view_config(route_name='downloadbuild')
    def downloadbuild(self):
        pb = self.get_db_object(PackBuild, perm=False)

        return Response(pb.build, content_type='application/json')
