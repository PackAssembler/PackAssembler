from .common import MMLServerView, VERROR, validate_captcha, opt_dict
from pyramid.view import view_config, forbidden_view_config
from ..security import check_pass, password_hash
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from random import getrandbits
from mandrill import Mandrill
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
            password = password_hash(post.get('txtPassword', ''))

            captcha_pass, captcha_error = validate_captcha(self.request, post.get('recaptcha_challenge_field', ''), post.get('recaptcha_response_field', ''))
            if captcha_pass:
                if username.isalnum() and email and password:
                    try:
                        user = User(username=username, password=password, email=email, groups=['group:user'], activate=getrandbits(32)).save()
                        self.send_confirmation(user)
                        return self.success_url('login', 'Successfully created an account please check your email to activate it.')
                    except ValidationError:
                        error = VERROR
                    except NotUniqueError:
                        error = 'Username or Email Already in Use.'
                else:
                    error = VERROR
            else:
                error = captcha_error
        return self.return_dict(title='Signup', error=error)

    @view_config(route_name='activate')
    def activate(self):
        user = self.get_db_object(User, perm=False)

        if user.activate == int(self.request.matchdict['key']):
            user.activate = None
            user.save()
            return HTTPFound(location=self.request.route_url('login'))
        else:
            return Response('Key Incorrect')

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

    @view_config(route_name='edituser', renderer='edituser.mak', permission='user')
    def edituser(self):
        error = ''
        post = self.request.params

        # Get user
        user = self.get_db_object(User)

        if 'btnSubmit' in post:
            if check_pass(self.logged_in, post['txtCurrentPassword']):
                params = opt_dict(password=password_hash(post.get('txtNewPassword')))
                if 'password' in params:
                    try:
                        for key in params:
                            if user[key] != params[key]:
                                user[key] = params[key]
                        user.save()
                        return HTTPFound(location=self.request.route_url('profile', id=user.id))
                    except ValidationError:
                        error = VERROR
            else:
                error = "Please enter your current password correctly."
        return self.return_dict(title="Edit Account", error=error)

    @view_config(route_name='deleteuser', permission='user')
    def deleteuser(self):
        # Get user
        user = self.get_db_object(User)

        orphan = self.get_orphan_user()

        Mod.objects(owner=user).update(set__owner=orphan)
        Pack.objects(owner=user).update(set__owner=orphan)
        Server.objects(owner=user).update(set__owner=orphan)

        user.delete()
        return HTTPFound(location=self.request.route_url('home'), headers=forget(self.request))

    @view_config(route_name='profile', renderer='profile.mak')
    def profile(self):
        # Get user
        user = self.get_db_object(User, perm=False)

        return self.return_dict(title=user.username, owner=user, mods=Mod.objects(owner=user),
                                packs=Pack.objects(owner=user), servers=Server.objects(owner=user),
                                perm=self.has_perm(user))

    def send_confirmation(self, user):
        sender = Mandrill('tv_A60S7VKgqFx8IPcENHg')
        message = {
            'to': [{'email': user.email, 'name': user.username}],
            'global_merge_vars': [{'content': self.request.route_url('activate', id=user.id, key=user.activate), 'name': 'confirmaddress'}]
        }
        sender.messages.send_template(template_name='confirmmcm', template_content=[], message=message, async=True)