from .schema import *
from wtforms import *
import htmllaundry
import re

# Form validators
def isalpha(form, field):
    if not field.data.isalpha():
        raise ValidationError('Field must only be composed of letters in the alphabet.')

def isalnum(form, field):
    if not field.data.isalnum():
        raise ValidationError('Field must be alphanumeric.')

def isforge(form, field):
    if not re.match('^([0-9]{1,2}\.){3}[0-9]{3}$', field.data):
        raise ValidationError('Not a valid forge version.')


# Common field creators
# Additional validators can be given with the v kwarg

def mcvfield(name, **kwargs):
    return SelectField(name, choices=[(v,v) for v in MCVERSIONS], **kwargs)

def targetfield(name, **kwargs):
    return SelectField(name, choices=[('both', 'Server and Client'), ('server', 'Server'), ('client', 'Client')], **kwargs)

def textfield_creator(default_validators):
    def creator(name, v=[], **kwargs):
        return TextField(name, validators=default_validators+v, **kwargs)
    return creator

forgefield = textfield_creator([isforge])
urlfield = textfield_creator([validators.URL()])
emailfield = textfield_creator([validators.Email()])
idfield = textfield_creator([validators.Regexp('^[0-9a-f]{24}$')])
namefield = textfield_creator([validators.required(), validators.Length(max=32), validators.Regexp('^[\w ]+$')])


# Subclassed form
class SForm(Form):
    def populate_obj(self, obj):
        for name, field in self._fields.items():
            if field.data:
                field.populate_obj(obj, name)
            else:
                setattr(obj, name, None)

# Safer TextAreaField
class SafeTextAreaField(TextAreaField):
    def pre_validate(self, form):
        self.data = htmllaundry.sanitize(self.data, cleaner=htmllaundry.cleaners.CommentCleaner)

# Mods
class ModForm(SForm):
    name = namefield('Name')
    author = TextField('Author', validators=[validators.Optional(), validators.Length(max=32)])
    install = TextField('Install', validators=[validators.required(), isalnum])
    url = urlfield('Homepage', v=[validators.required()])
    target = targetfield('Target')
    permission = SafeTextAreaField('Permission')

class ModVersionForm(SForm):
    version = TextField('Version', validators=[validators.required()])
    mc_min = mcvfield('Minecraft Min')
    mc_max = mcvfield('Minecraft Max')
    forge_min = forgefield('Forge Min', v=[validators.Optional()])
    forge_max = forgefield('Forge Max', v=[validators.Optional()])

# Packs
class PackForm(SForm):
    name = namefield('Name')

class PackModForm(SForm):
    id = idfield('Mod ID', v=[validators.required()])

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
    port = IntegerField('Port', validators=[validators.required(), validators.NumberRange(max=65535)])
    packid = idfield('Pack ID', v=[validators.required()])
    revision = IntegerField('Pack Revision', validators=[validators.required()])
    config = urlfield('Custom Config', v=[validators.Optional()])

# Users
class UserForm(SForm):
    username = TextField('Username', validators=[validators.required(), validators.Length(min=6, max=32), isalnum])
    email = emailfield('Email', v=[validators.required()])
    password = PasswordField('Password', validators=[validators.required()])
    confirm = PasswordField('Confirm', validators=[validators.required(), validators.EqualTo('password', 'Field must be same as password.')])

class LoginForm(SForm):
    username = TextField('Username', validators=[validators.required()])
    password = PasswordField('Password', validators=[validators.required()])
    came_from = HiddenField()

class SendResetForm(SForm):
    email = emailfield('Email', v=[validators.required()])

    def validate_email(form, field):
        if User.objects(email=field.data).first() == None:
            raise ValidationError('No user with that email exists.')

class ResetForm(SForm):
    password = PasswordField('New Password', validators=[validators.required()])
    confirm = PasswordField('Confirm', validators=[validators.required(), validators.EqualTo('password', 'Field must be same as password.')])

class EditUserForm(ResetForm):
    current = PasswordField('Current Password', validators=[validators.required()])
    current_user = HiddenField()

    def validate_current(form, field):
        if not check_pass(form.current_user.data, field.data):
            raise ValidationError('Current password incorrect.')
