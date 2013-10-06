from .common import ViewBase, url_md5
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from lxml.builder import ElementMaker
from pyramid.view import view_config
from ..form import PackBuildForm
from lxml.etree import tostring
from ..schema import *


VERSION_KEY = 'forgeversions'


class PackBuildViews(ViewBase):

    def linkerror(self, mod, message):
        return '<a href="' + self.request.route_url('viewmod', id=mod.id) + '">' + mod.name + '</a>' + ' ' + message

    @view_config(route_name='addbuild', renderer='addbuild.mak', permission='user')
    def addbuild(self):
        error = ''
        pack = self.get_db_object(Pack)
        post = self.request.params
        form = PackBuildForm(post)

        if 'submit' in post and form.validate():
            elist = []

            splitm = form.mc_version.data.split('.')
            splitf = form.forge_version.data.split('.')

            mod_versions = []

            for mod in pack.mods:
                mc_compat = [i for i in mod.versions
                             if i.mc_min.split('.') <= splitm
                             and i.mc_max.split('.') >= splitm]
                if mc_compat:
                    forge_compat = []
                    for version in mc_compat:
                        dversion = version.to_mongo()
                        forge_min = dversion.get(
                            'forge_min', '0.0.0.000').split('.')
                        forge_max = dversion.get(
                            'forge_max', '9.9.9.999').split('.')
                        if forge_min <= splitf and forge_max >= splitf:
                            forge_compat.append(version)
                    if forge_compat:
                        dcompat = [
                            version for version in forge_compat if version.devel is False or pack.devel is True]
                        if dcompat:
                            selected = max(
                                dcompat, key=lambda v: v.version.split('.'))
                        else:
                            selected = max(
                                forge_compat, key=lambda v: v.version.split('.'))
                        mod_versions.append(selected)
                    else:
                        elist.append(self.linkerror(mod, 'is incompatible with Forge ' +
                                     form.forge_version.data))
                else:
                    elist.append(self.linkerror(mod, 'is incompatible with Minecraft ' +
                                 form.mc_version.data))
            if elist:
                error = '<ul>'
                for e in elist:
                    error += '<li>' + e + '</li>'
                error += '</ul>'
            else:
                pb = PackBuild(
                    mod_versions=mod_versions, mc_version=form.mc_version.data,
                    forge_version=form.forge_version.data, pack=pack, revision=pack.latest + 1)
                if form.config.data:
                    pb.config = form.config.data
                pb.save()
                pack.latest = pb.revision
                pack.builds.append(pb)
                pack.save()
                return HTTPFound(self.request.route_url('viewpack', id=pack.id))

        return self.return_dict(title='New Build', error=error, f=form, cancel=self.request.route_url('viewpack', id=pack.id))

    @view_config(route_name='deletebuild', permission='user')
    def deletebuild(self):
        pb = self.get_db_object(PackBuild)

        if self.check_depends(pb):
            pb.delete()
            return HTTPFound(location=self.request.referer)
        else:
            return HTTPFound(self.request.route_url('error', type='depends'))

    @view_config(route_name='downloadbuild', renderer='json')
    def downloadbuild(self):
        pb = self.get_db_object(PackBuild, perm=False)
        jdict = {
            'pack_id': str(pb.pack.id),
            'pack_name': pb.pack.name,
            'config': pb.config,
            'mc_version': pb.mc_version,
            'forge_version': pb.forge_version,
            'mods': {}
        }
        for mv in pb.mod_versions:
            jdict['mods'][str(mv.mod.id)] = {
                'name': mv.mod.name,
                'target': mv.mod.target,
                'version': str(mv.id)
            }

        return jdict

    @view_config(route_name='mcuxml')
    def mcuxml(self):
        pb = self.get_db_object(PackBuild, perm=False)

        return Response(generate_mcu_xml(self.request, pb), content_type='application/xml')

    @view_config(route_name='paq')
    def paq(self):
        pb = self.get_db_object(PackBuild, perm=False)

        resp = ''
        for mv in pb.mod_versions:
            resp += self.request.route_url('downloadversion', id=mv.id)
            resp += '\nfalse\nfalse\nPAQ-Temp/mods\nPAQ-Temp/mods\n'
            resp += mv.mod.rid + '.zip\n'

        if pb.config:
            resp += pb.config + '\nfakse\ntrue\nPAQ-Temp/downloads\nPAQ-Temp/config\nconfig.zip\n'

        forge_filename = 'minecraftforge-installer-{0}-{1}.jar'.format(pb.mc_version, pb.forge_version)
        forge_url = 'http://files.minecraftforge.net/minecraftforge/' + forge_filename
        resp += forge_url + '\n' + forge_filename + '\n' + '{0}-Forge{1}'.format(pb.mc_version, pb.forge_version)

        return Response(resp, content_type='text/plain')

    @view_config(route_name='forgeversions', renderer='json')
    def forgeversions(self):
        build_data = Setting.objects.get(key=VERSION_KEY).build_data
        mc_version = self.request.GET['mc_version'].replace('.', '_')

        return build_data[mc_version]


def generate_mcu_xml(request, pb, server=None):
    E = ElementMaker(nsmap={
        'noNamespaceSchemaLocation': 'http://www.mcupdater.com/ServerPack',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'schemaLocation': 'http://www.mcupdater.com/ServerPackv2.xsd'})

    # Create server tag attributes
    server_info = {
        'revision': str(pb.revision),
        'version': pb.mc_version,
        'mainClass': 'net.minecraft.launchwrapper.Launch'
    }
    # If this is a server, use server information
    if server:
        server_info['id'] = 'server-' + server.rid
        server_info['name'] = server.name
        server_info['newsUrl'] = server.url or request.route_url(
            'viewpack', id=pb.pack.id)
        server_info['serverAddress'] = '{0}:{1}'.format(
            server.host, str(server.port))
    # If it's not, use the pack information
    else:
        server_info['id'] = pb.pack.rid
        server_info['name'] = pb.pack.name
        server_info['newsUrl'] = request.route_url('viewpack', id=pb.pack.id)
        server_info['serverAddress'] = 'localhost'
        server_info['autoConnect'] = 'false'

    # Create the base xml
    xml = E.ServerPack(
        E.Server(
            E.Import(
                'forge', {'url': 'http://files.mcupdater.com/example/forge.php?mc={0}&forge={1}'.format(pb.mc_version, pb.forge_version)}),
            server_info
        ),
        {'version': '3.0'}
    )

    # Add the mods
    for mv in pb.mod_versions:
        xml[0].append(mod_xml(E, request, mv))

    # Get the config url, if there is none in either server or pack, leave it
    # blank
    config_url = ''
    if server:
        if server.config:
            config_url = server.config
    else:
        if pb.config:
            config_url = pb.config

    # If we've got a config, add it as if it were a mod
    if config_url:
        xml[0].append(E.Module(
            E.URL(config_url),
            E.Required('true'),
            E.ModType('Extract', {'inRoot': 'true'}),
            E.MD5(url_md5(config_url)[0]),
            {
                'id': 'Config',
                'name': 'Config'
            }
        ))

    return tostring(xml)


def mod_xml(E, request, mv):
    return E.Module(
        E.URL(request.route_url('downloadversion', id=mv.id)),
        E.Required('true'),
        E.ModType('Regular'),
        E.MD5(mv.mod_file.md5 if mv.mod_file else mv.mod_file_url_md5),
        {
            'id': mv.mod.rid,
            'name': '{0} ({1})'.format(mv.mod.name, mv.version),
        }
    )
