from pyramid.view import view_config, notfound_view_config
from pyramid.httpexceptions import HTTPNotFound
from .common import ViewBase


class GeneralViews(ViewBase):
    # General

    @view_config(route_name='home', renderer='home.mak')
    def home(self):
        return self.return_dict(title='Home')

    @view_config(route_name='faq', renderer='faq.mak')
    def faq(self):
        return self.return_dict(title='FAQ')

    @view_config(route_name='gettingstarted', renderer='gettingstarted.mak')
    def gettingstarted(self):
        return self.return_dict(title='Getting Started')

    @notfound_view_config(append_slash=True)
    def notfound(self):
        return HTTPNotFound()
