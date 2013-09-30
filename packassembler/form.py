from .security import check_pass
from .schema import *
from wtforms import *
import htmllaundry
import re


# Form validators

def isalpha(form, field):
    if not field.data.isalpha():
        raise ValidationError(
            'Field must only be composed of letters in the alphabet.')


def isalnum(form, field):
    if not field.data.isalnum():
        raise ValidationError('Field must be alphanumeric.')


def isforge(form, field):
    if not re.match('^([0-9]{1,2}\.){3}[0-9]{3}$', field.data):
        raise ValidationError('Not a valid forge version.')


def iscolor(form, field):
    if not re.match('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', field.data):
        raise ValidationError('Not a valid hex color code.')


# Form widgets

class ColorInput(widgets.core.Input):

    """ Renders an input with type "color". """
    input_type = 'color'


# Form fields

class ColorField(fields.core.StringField):

    """ Represents an ``<input type="color">``. """
    widget = ColorInput()


# Common field creators
# Additional validators can be given with the v kwarg

def mcvfield(name, **kwargs):
    return SelectField(name, choices=[(v, v) for v in MCVERSIONS], **kwargs)


def targetfield(name, **kwargs):
    return SelectField(name, choices=[('both', 'Server and Client'), ('server', 'Server'), ('client', 'Client')], **kwargs)


def textfield_creator(default_validators):
    def creator(name, v=[], **kwargs):
        return TextField(name, validators=v + default_validators, **kwargs)
    return creator

forgefield = textfield_creator([isforge])
urlfield = textfield_creator([validators.URL()])
emailfield = textfield_creator([validators.Email()])
idfield = textfield_creator([validators.Regexp('^[0-9a-f]{24}$')])
namefield = textfield_creator(
    [validators.required(), validators.Length(max=32), validators.Regexp('^[\w ]+$')])


# Specific Validators

def validate_current(form, field):
    """Validator for operations which require password."""
    if not check_pass(form.current_user.data, field.data):
        raise ValidationError('Current password incorrect.')


def either_mod_file(form, field):
    """Checks to see if file upload or url field is filled."""
    message = 'Must have either File or File URL filled.'
    try:
        file_not_entered = not form.mod_file.data.file
    except AttributeError:
        file_not_entered = True

    if file_not_entered and not field.data:
        raise validators.StopValidation(message)


# Subclassed form

class SForm(Form):

    def populate_obj(self, obj):
        for name, field in self._fields.items():
            if not field.__class__.__name__ == 'FileField':
                if field.data:
                    field.populate_obj(obj, name)
                else:
                    setattr(obj, name, None)


# Safer TextAreaField

class SafeTextAreaField(TextAreaField):

    def pre_validate(self, form):
        c = htmllaundry.cleaners.DocumentCleaner
        c.allow_tags.append('div')
        self.data = htmllaundry.sanitize(self.data, cleaner=c, wrap=None)


# TextAreaField, no HTML allowed

class ParanoidTextAreaField(TextAreaField):

    def pre_validate(self, form):
        self.data = htmllaundry.strip_markup(self.data)


# Mods

class ModForm(SForm):
    name = namefield('Name')
    description = SafeTextAreaField('Description')
    author = TextField('Author', validators=[
                       validators.required(), validators.Length(max=32)])
    url = urlfield('Homepage', v=[validators.required()])
    target = targetfield('Target')
    permission = ParanoidTextAreaField('Permission')


class BannerForm(SForm):
    image = urlfield('Image URL', v=[validators.Optional()])
    text_color = ColorField(
        'Text Color', validators=[validators.Optional(), iscolor])


class ModVersionForm(SForm):
    version = TextField('Version', validators=[validators.required()])
    mc_min = mcvfield('Minecraft Min')
    mc_max = mcvfield('Minecraft Max')
    forge_min = forgefield('Forge Min', v=[validators.Optional()])
    forge_max = forgefield('Forge Max', v=[validators.Optional()])
    devel = BooleanField('Development Version')
    mod_file = FileField('File')
    mod_file_url = urlfield(
        'File URL', v=[either_mod_file, validators.Optional()])


class EditModVersionForm(ModVersionForm):
    mod_file_url = urlfield('File URL', v=[validators.Optional()])


# Packs

class PackForm(SForm):
    name = namefield('Name')
    devel = BooleanField('Use Development Versions')


# Pack Builds

class PackBuildForm(SForm):
    mc_version = mcvfield('Minecraft Version')
    forge_version = forgefield('Forge Version', v=[validators.required()])
    config = urlfield('Config', v=[validators.Optional()])


# Servers

class ServerForm(SForm):
    name = namefield('Name')
    url = urlfield('Homepage', v=[validators.Optional()])
    host = TextField('Host', validators=[validators.required()])
    port = IntegerField(
        'Port', validators=[validators.required(), validators.NumberRange(max=65535)])
    packid = idfield('Pack ID', v=[validators.required()])
    revision = IntegerField(
        'Pack Revision', validators=[validators.required()])
    config = urlfield('Custom Config', v=[validators.Optional()])


# Users
# Not logged in

class UserForm(SForm):
    username = TextField('Username', validators=[
                         validators.required(), validators.Length(min=6, max=32), isalnum])
    email = emailfield('Email', v=[validators.required()])
    password = PasswordField('Password', validators=[validators.required()])
    confirm = PasswordField('Confirm', validators=[
                            validators.required(), validators.EqualTo('password', 'Field must be same as password.')])


class LoginForm(SForm):
    username = TextField('Username', validators=[validators.required()])
    password = PasswordField('Password', validators=[validators.required()])
    came_from = HiddenField()


class SendResetForm(SForm):
    email = emailfield('Email', v=[validators.required()])

    def validate_email(form, field):
        if User.objects(email=field.data).first() is None:
            raise ValidationError('No user with that email exists.')


class ResetForm(SForm):
    password = PasswordField(
        'New Password', validators=[validators.required()])
    confirm = PasswordField('Confirm', validators=[
                            validators.required(), validators.EqualTo('password', 'Field must be same as password.')])


# Logged in

class EditUserPasswordForm(ResetForm):
    current = PasswordField(
        'Current Password', validators=[validators.required(), validate_current])
    current_user = HiddenField()


class EditUserEmailForm(SForm):
    email = emailfield('Email', v=[validators.required()])
    current_user = HiddenField()
    current = PasswordField(
        'Current Password', validators=[validators.required(), validate_current])


class EditUserAvatarForm(SForm):
    avatar_type = SelectField(
        'Avatar', choices=[('0', 'Gravatar'), ('1', 'Minotar')], validators=[validators.required()])
