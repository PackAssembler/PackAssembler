from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from .common import ViewBase, url_md5
from pyramid.view import view_config
from ..schema import *
#import requests


class PackBuildViews(ViewBase):

    @view_config(route_name='technic_packlist', renderer='json')
    def technic_packlist(self):
        rdict = {'modpacks': {}, 'mirror_url': 'http://mml.stephenmac.com/technic/api/repo/'}
        for pack in Pack.objects:
            rdict['modpacks'][pack.rid] = pack.name
        return rdict

    @view_config(route_name='technic_viewpack', renderer='json')
    def technic_viewpack(self):
        pack = Pack.objects.get(rid=self.request.matchdict['rid'])
        latest = pack.builds[-1].revision if pack.builds else None
        rdict = {
            'name': pack.rid,
            'display_name': pack.name,
            'url': self.request.route_url('viewpack', id=pack.id),
            'icon_md5': '4c4e1c99f5827d64b9eceef8ee75e05e',
            'logo_md5': '3bee0e2d79c78f760f9d3ab98d61630a',
            'background_md5': '6d919f395e92bc72522cb6b45d98ab57',
            'recommended': latest,
            'latest': latest,
            'builds': []
        }
        for build in pack.builds:
            rdict['builds'].append(build.revision)
        return rdict

    @view_config(route_name='technic_viewbuild', renderer='json')
    def technic_viewbuild(self):
        pb = PackBuild.objects.get(
            pack=Pack.objects.get(rid=self.request.matchdict['rid']), revision=self.request.matchdict['revision'])
        rdict = {
            'minecraft': pb.mc_version,
            'mods': [],
            'forge': pb.forge_version
        }
        for mv in pb.mod_versions:
            rdict['mods'].append({
                'name': str(mv.mod.rid),
                'version': mv.version,
                'md5': (mv.mod_file.md5 if mv.mod_file else mv.mod_file_url_md5),
                'url': self.request.route_url('downloadversion', id=mv.id),
                'location': 'mods'
            })
        if pb.config:
            rdict['mods'].append({
                'name': 'config',
                'version': str(pb.revision),
                'md5': url_md5(pb.config)[0],
                'url': pb.config,
                'extract': True
            })
        return rdict

    @view_config(route_name='technic_repo')
    def technic_repo(self):
        image = self.request.matchdict['image']
        if image == 'background.jpg':
            return HTTPFound(location='http://placekitten.com/800/510')
        elif image == 'icon.png':
            return HTTPFound(location='http://placekitten.com/32/32')
        elif image == 'logo_180.png':
            return HTTPFound(location='http://placekitten.com/180/110')
        else:
            return HTTPBadRequest()
