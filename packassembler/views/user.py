from ..form import UserForm, LoginForm, SendResetForm, ResetForm, EditUserPasswordForm, EditUserAvatarForm, EditUserEmailForm, EmailUserForm
from .common import ViewBase, validate_captcha
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from ..security import check_pass, password_hash
from pyramid.security import remember, forget
import packassembler.views.email as email
from pyramid.response import Response
from random import getrandbits
from datetime import datetime
from hashlib import md5
from ..schema import *

ehash = lambda e: md5(e.strip().encode()).hexdigest()


class UserViews(ViewBase):

    @view_config(route_name='userlist', renderer='userlist.mak')
    def userlist(self):
        post = self.request.params

        if 'q' in post:
            users = User.objects(username__icontains=post['q'])
        else:
            users = User.objects

        return self.return_dict(title="Users", users=users)

    @view_config(route_name='signup', renderer='signup.mak')
    def signup(self):
        error = ''
        post = self.request.params
        form = UserForm(post)

        # Make sure no one is logged in
        if self.logged_in is not None:
            return HTTPFound(location=self.request.route_url('home'))

        if 'submit' in post and form.validate():
            password = password_hash(form.password.data)
            captcha_pass, captcha_error = validate_captcha(self.request)

            if captcha_pass:
                try:
                    user = User(username=form.username.data,
                                password=password,
                                email=form.email.data,
                                email_hash=ehash(form.email.data),
                                activate=getrandbits(32)).save()
                    self.send_confirmation(user)

                    self.request.session.flash('Successfully created an account please check your email to activate it.')
                    return HTTPFound(self.request.route_url('login'))
                except NotUniqueError:
                    error = 'Username or Email Already in Use.'
            else:
                error = captcha_error

        return self.return_dict(title='Signup', error=error, f=form)

    @view_config(route_name='activate')
    def activate(self):
        user = self.get_db_object(User, perm=False)

        if user.activate == int(self.request.matchdict['key']):
            user.activate = None
            user.save()

            self.request.session.flash('Account activated. Please login.')
        else:
            self.request.session.flash('Invalid Key.', 'errors')

        return HTTPFound(self.request.route_url('login'))

    @view_config(route_name='login', renderer='login.mak')
    @forbidden_view_config(renderer='login.mak')
    def login(self):
        error = ''
        post = self.request.params
        form = LoginForm(post)

        # Get referrer
        referrer = self.request.url
        if referrer == self.request.route_url('login'):
            referrer = '/'
        came_from = post.get('came_from', referrer)
        form.came_from.data = came_from

        # Make sure no one is logged in
        if self.logged_in is not None:
            # If this is happening because the user has no permission
            if isinstance(self.request.exception, HTTPForbidden):
                self.request.session.flash('You may not create nor adopt mods unless you are a contributor.', 'errors')
            return HTTPFound(self.request.route_url('home'))

        if 'submit' in post and form.validate():
            username = form.username.data
            user = check_pass(username, form.password.data)
            if user:
                user.last_login = datetime.now()
                user.save()
                return HTTPFound(location=came_from, 
                    headers=remember(self.request, user.username))
            error = 'Invalid username or password.'

        return self.return_dict(title='Login', error=error, f=form)

    @forbidden_view_config(renderer='json', xhr=True)
    def forbidden_json(self):
        return {'success': False, 'error': 'not_logged_in'}

    @view_config(route_name='logout')
    def logout(self):
        return HTTPFound(location=self.request.referer, headers=forget(self.request))

    @view_config(route_name='sendreset', renderer='genericform.mak')
    def sendreset(self):
        post = self.request.params
        form = SendResetForm(post)

        if 'submit' in post and form.validate():
            user = User.objects.get(email=form.email.data)
            user.reset = getrandbits(32)
            user.save()

            self.send_password_reset(user)

            self.request.session.flash('Please check your email to continue resetting your password.')
            return HTTPFound(self.request.route_url('login'))

        return self.return_dict(title='Forgot Password', f=form, cancel=self.request.route_url('login'))

    @view_config(route_name='reset', renderer='genericform.mak')
    def reset(self):
        user = self.get_db_object(User, perm=False)
        post = self.request.params
        form = ResetForm(post)

        # Make sure the key is correct
        if user.reset != int(self.request.matchdict['key']):
            return Response('Invalid Key')

        if 'submit' in post and form.validate():
            user.password = password_hash(form.password.data)
            user.reset = None
            user.save()

            self.request.session.flash('Password reset successfully.')
            return HTTPFound(self.request.route_url('login'))

        return self.return_dict(title='Reset Password', f=form, cancel=self.request.route_url('login'))

    @view_config(route_name='emailuser', renderer='genericform.mak', permission='user')
    def emailuser(self):
        user = self.get_db_object(User, perm=False)
        post = self.request.params
        form = EmailUserForm(post)

        if 'submit' in post and form.validate():
            email.user_email(self.request.registry, user, self.current_user, form.message.data)

            return HTTPFound(self.request.route_url('profile', id=user.id))

        return self.return_dict(title='Send Email to ' + user.username, f=form, cancel=self.request.route_url('profile', id=user.id))

    @view_config(route_name='edituser', renderer='edituser.mak', permission='user')
    def edituser(self):
        user = self.get_db_object(User)
        post = self.request.params

        # Create forms
        password_form = EditUserPasswordForm(post)
        email_form = EditUserEmailForm(post)
        avatar_form = EditUserAvatarForm(post, user)

        password_form.current_user.data = self.logged_in
        email_form.current_user.data = self.logged_in

        rval = HTTPFound(
            location=self.request.route_url(
                'profile',
                id=user.id))
        if 'password_submit' in post and password_form.validate():
            user.password = password_hash(password_form.password.data)
            user.save()
            return rval

        elif 'email_submit' in post and email_form.validate():
            user.email = email_form.email.data
            user.email_hash = ehash(email_form.email.data)
            try:
                user.save()
                return rval
            except NotUniqueError:
                email_form.email.errors.append('Email not unique.')

        elif 'avatar_submit' in post and avatar_form.validate():
            avatar_form.populate_obj(user)
            user.save()
            return rval

        elif 'group' in post and self.specperm('admin'):
            user.group = post['group']
            user.save()
            return rval

        return self.return_dict(
            title="Edit Account", pf=password_form,
            ef=email_form, af=avatar_form,
            cancel=self.request.route_url('profile', id=user.id)
        )

    @view_config(route_name='deleteuser', permission='user')
    def deleteuser(self):
        # Get user
        user = self.get_db_object(User)

        orphan = self.get_orphan_user()
        Mod.objects(owner=user).update(set__owner=orphan)

        user.delete()

        self.request.session.flash('User deleted successfully.')
        headers = forget(self.request) if self.logged_in == user.username else None
        return HTTPFound(location=self.request.route_url('home'), headers=headers)

    @view_config(route_name='profile', renderer='profile.mak')
    def profile(self):
        # Get user
        user = self.get_db_object(User, perm=False)

        return self.return_dict(
            title=user.username, owner=user, mods=Mod.objects(owner=user),
            packs=Pack.objects(owner=user), servers=Server.objects(owner=user),
            perm=self.has_perm(user), admin=self.specperm('admin'))

    def send_confirmation(self, user):
        url = self.request.route_url('activate', id=user.id, key=user.activate)
        email.confirmation(self.request.registry, user, url)

    def send_password_reset(self, user):
        url = self.request.route_url('reset', id=user.id, key=user.reset)
        email.password_reset(self.request.registry, user, url)
