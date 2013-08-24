from wtforms import *

# Form validators
def isalpha(form, field):
    if not field.data.isalpha():
        raise ValidationError('Field must only be composed of letters in the alphabet.')


def isalnum(form, field):
    if not field.data.isalnum():
        raise ValidationError('Field must be alphanumeric.')
