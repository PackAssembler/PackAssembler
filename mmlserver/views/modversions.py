from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from .common import MMLServerView, opt_dict
from pyramid.response import Response
from pyramid.view import view_config
from ..schema import *
import re


class MMLServerVersions(MMLServerView):
    @view_config(route_name='addversion', renderer='editmodversion.mak', permission='user')
    def addversion(self):
        error = ''
        post = self.request.params
        mod = Mod.objects.get(id=self.request.matchdict['modid'])
        if mod is None:
            return HTTPNotFound()
        if 'btnSubmit' in post:
            params = opt_dict(
                mc_min=post.get('selMCMin'),
                mc_max=post.get('selMCMax'),
                forge_min=post.get('txtForgeMin'),
                forge_max=post.get('txtForgeMax'),
                version=post.get('txtVersion'),
                mod_file=post.get('uplModFile').file
            )
            check_forge = lambda x: re.match('^([0-9]\.){3}[0-9]{3}$', params[x]) is not None if x in params else True
            if check_forge('forge_min') and check_forge('forge_max'):
                if not self.has_perm(mod):
                    error = 'You do not have permission to add a version.'
                else:
                    mv = ModVersion(mod=mod, **params).save()
                    mod.versions.append(mv)
                    mod.save()
                    return HTTPFound(location=self.request.route_url('viewmod', modid=self.request.matchdict['modid']))
            else:
                error = 'Forge values not correctly defined.'
        return self.return_dict(title="Add Mod Version", error=error)

    @view_config(route_name='editversion', renderer='editmodversion.mak', permission='user')
    def editversion(self):
        error = ''
        post = self.request.params
        mv = ModVersion.objects.get(id=self.request.matchdict['versionid'])
        if mv is None:
            return HTTPNotFound()
        if 'btnSubmit' in post:
            params = opt_dict(
                mc_min=post.get('selMCMin'),
                mc_max=post.get('selMCMax'),
                forge_min=post.get('txtForgeMin'),
                forge_max=post.get('txtForgeMax'),
                version=post.get('txtVersion')
            )
            try:
                params['mod_file'] = post.get('uplModFile').file
            except AttributeError:
                pass
            check_forge = lambda x: re.match('^([0-9]\.){3}[0-9]{3}$', params[x]) is not None if x in params else True
            if check_forge('forge_min') and check_forge('forge_max'):
                if not self.has_perm(mv.mod):
                    error = 'You do not have permission to edit a version.'
                else:
                    for key in params:
                        if mv[key] != params[key]:
                            mv[key] = params[key]
                    mv.save()
                    return HTTPFound(location=self.request.route_url('viewmod', modid=mv.mod.id))
            else:
                error = 'Forge values not correctly defined.'
        return self.return_dict(title="Edit Mod Version", v=mv, error=error)

    @view_config(route_name='downloadversion')
    def downloadversion(self):
        d = self.request.matchdict
        mv = ModVersion.objects.get(id=d['versionid'])
        if mv is not None:
            return Response(mv.mod_file.read(), content_type='application/zip')
        else:
            return HTTPNotFound()

    @view_config(route_name='deleteversion', permission='user')
    def deleteversion(self):
        d = self.request.matchdict
        mv = ModVersion.objects.get(id=d['versionid'])
        if mv is not None and self.has_perm(mv.mod):
            mv.mod_file.delete()
            mv.delete()
            return HTTPFound(location=self.request.referer)
        else:
            return HTTPNotFound()
