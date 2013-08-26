from pyramid.view import view_config
from .common import MMLServerView


class MMLServerViews(MMLServerView):
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

    @view_config(route_name='success', renderer='success.mak')
    def success(self):
        d = self.request.params
        redir_url = self.request.route_url(d.get('redirect', 'home'))
        return self.return_dict(title='Success', message=d.get('message', 'Success'), redir=redir_url)

    @view_config(route_name='error', renderer='error.mak')
    def error(self):
        e = self.request.matchdict['type']
        if e == 'depends':
            return self.return_dict(title='Unable to Delete', message='Unable to delete the requested object.' + 
                                    ' Something depends on it. If you would not like to maintain it any longer, please disown it.')
        elif e == 'not_trusted':
            return self.return_dict(title='Not Trusted User', message='You may not create nor adopt mods unless you are a trusted user.')
        elif e == 'already_cloned':
            return self.return_dict(title='Already Cloned', message='It seems that you have already cloned this pack. To make another, change the name of your other clone.')
        else:
            return self.return_dict(title='Error', message='An unknown error has occured: ' + e)
