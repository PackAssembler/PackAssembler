from pyramid.view import view_config
from .common import MMLServerView


class MMLServerViews(MMLServerView):
    # General
    @view_config(route_name='home', renderer='home.mak')
    def home(self):
        return self.return_dict(title='Home')

    @view_config(route_name='about', renderer='about.mak')
    def about(self):
        return self.return_dict(title='About')

    @view_config(route_name='gettingstarted', renderer='gettingstarted.mak')
    def gettingstarted(self):
        return self.return_dict(title='Getting Started')

    @view_config(route_name='success', renderer='success.mak')
    def success(self):
        d = self.request.params
        redir_url = self.request.route_url(d.get('redirect', 'home'))
        return self.return_dict(title='Success', message=d.get('message', 'Success'), redir=redir_url)
