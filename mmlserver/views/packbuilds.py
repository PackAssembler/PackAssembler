from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.view import view_config
from .common import MMLServerView
from ..schema import *


class MMLServerPackBuild(MMLServerView):
    @view_config(route_name='addbuild', renderer='editbuild.mak', permission='user')
    def addbuild(self):
        # Defaults
        error = ''
        return self.return_dict(title='New Build', error=error)
