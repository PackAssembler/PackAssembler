from .common import ViewBase
from pyramid.view import view_config
from datetime import datetime, timedelta
from ..schema import *


class AdminViews(ViewBase):
    @view_config(route_name='maintenance', renderer='admin/maintenance.mak', permission='admin', request_method='GET')
    def maintenance(self):
        return self.return_dict(title='Maintenance')

    @view_config(route_name='maintenance', renderer='admin/maintenance.mak', permission='admin', request_method='POST')
    def maintenance_post(self):
        if 'remove_old_users' in self.request.params:
            clean_users()
            self.request.flash('Old users removed.')
        elif 'remove_old_versions' in self.request.params:
            clean_versions()
            self.request.flash('Old versions removed.')
        return self.return_dict(title='Maintenance')


def clean_users():
    too_old = datetime.now() - timedelta(days=45)
    for user in User.objects:
        # The user has  never logged in or logged in more than 45 days ago
        ltime = not user.last_login or user.last_login < too_old
        # If the user is in the user group and has no mods, along with
        # not having logged in recently, delete 'em
        if not Mod.objects(owner=user) and user.group == 'user' and ltime:
            user.delete()


def clean_versions():
    for mod in Mod.objects:
        occupied = {'stable': [], 'devel': []}
        for version in mod.versions[::-1]:
            occ_list = occupied['devel' if version.devel else 'stable']
            if version.mc_version in occ_list:
                print('Will delete {0} {1}'.format(mod.name, version.version))
            else:
                occ_list.append(version.mc_version)
