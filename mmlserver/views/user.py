from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember, forget
from .common import MMLServerView, VERROR
from pyramid.response import Response
from ..security import check_pass
from ..schema import *


class MMLServerUser(MMLServerView):
    @view_config(route_name='signup', renderer='signup.mak')
    def signup(self):
        error = ''
        post = self.request.params

        # Make sure no one is logged in
        if self.logged_in is not None:
            return HTTPFound(location=self.request.route_url('home'))

        if 'btnSubmit' in post:
            username = post.get('txtUsername', '')
            email = post.get('txtEmail', '')
            password = post.get('txtPassword', '')
            if username.isalnum() and email and password:
                try:
                    User(username=username, password=password.encode(), email=email, groups=['group:user']).save()
                    return self.success_url('login', 'Successfully created an account.')
                except ValidationError:
                    error = VERROR
                except NotUniqueError:
                    error = username + ' is taken'
            else:
                error = VERROR
        return self.return_dict(title='Signup', error=error)

    @view_config(route_name='taken')
    def taken(self):
        if User.objects(username=self.request.params['txtUsername']).first() is None:
            return Response('1')
        else:
            return Response('0')

    @view_config(route_name='login', renderer='login.mak')
    @forbidden_view_config(renderer='login.mak')
    def login(self):
        error = ''
        post = self.request.params

        # Check referrer
        referrer = self.request.url
        if referrer == self.request.route_url('login'):
            referrer = '/'
        came_from = post.get('came_from', referrer)

        # Make sure no one is logged in
        if self.logged_in is not None:
            return HTTPFound(location=self.request.route_url('home'))

        if 'btnSubmit' in post:
            username = post.get('txtUsername', '')
            password = post.get('txtPassword', '')
            if check_pass(username, password):
                return HTTPFound(location=came_from, headers=remember(self.request, username))
            error = 'Invalid username or password.'
        return self.return_dict(title='Login', error=error, came_from=came_from)

    @view_config(route_name='logout')
    def logout(self):
        return HTTPFound(location=self.request.referer, headers=forget(self.request))

    @view_config(route_name='profile', renderer='profile.mak')
    def profile(self):
        try:
            user = User.objects.get(id=self.request.matchdict['userid'])
        except DoesNotExist:
            return HTTPNotFound()

        return self.return_dict(title=user.username, mods=Mod.objects(owner=user),
                                packs=Pack.objects(owner=user), servers=Server.objects(owner=user))
