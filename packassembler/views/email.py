# SMTP
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message


def smtpify(f):

    def smtpified(request, user, *args, **kwargs):
        sender = get_mailer(request)

        to = "{0} <{1}>".format(user.username, user.email)
        message = f(Message(recipients=[to]), *args, **kwargs)

        sender.send_immediately(message)

    return smtpified


@smtpify
def password_reset(message, reset_url):
    message.subject = "Reset Your Password"
    message.html = """
Reset your password by clicking the link below:<br/>
<a href="{0}">{0}</a><br/><br/>

If you did not request to reset your Pack Assembler password, please ignore
this message and login to invalidate the reset code.
""".format(reset_url)
    message.body = """
Reset your password by copying and pasting the link below:
{0}

If you did not request to reset your Pack Assembler password, please ignore
this message and login to invalidate the reset code.
""".format(reset_url)
    return message


@smtpify
def confirmation(message, activate_url):
    message.subject = "Confirm Your Email"
    message.html = """
Confirm that you own this email by clicking the link below:<br/>
<a href="{0}">{0}</a><br/><br/>

If you did not request to be signed up for Pack Assembler, please ignore this
message.
""".format(activate_url)
    message.body = """
Confirm that you own this email by by copying and pasting the link below:
{0}

If you did not request to be signed up for Pack Assembler, please ignore this
message.
""".format(activate_url)
    return message


@smtpify
def mod_outdated(message, mod_name, mod_url):
    message.subject = "Outdated Mod - " + mod_name
    message.html = """
A mod you maintain, {0} has been marked as outdated. To update it, click on the
link below:<br/>
<a href="{1}">{1}</a>
""".format(mod_name, mod_url)
    message.body = """
A mod you maintain, {0} has been marked as outdated. To update it, copy and
paste the link below:
{1}
""".format(mod_name, mod_url)
    return message


@smtpify
def user_email(message, sender, message_body):
    message.subject = sender.username + ' on Pack Assembler has sent you a message'
    message.headers = {'Reply-To', sender.email}
    message.body = """
You have been sent a message by {0} on Pack Assembler:
{1}
""".format(sender.username, message_body)
    return message


# Mandrill
# from mandrill import Mandrill


# def mandrillify(template):

#     def dec(f):

#         def mandrilled(request, user, *args, **kwargs):
#             sender = Mandrill(request.registry.settings.get('mandrill_key'))

#             message = {'to': [{'email': user.email, 'name': user.username}]}

#             rval = f(*args, **kwargs)
#             if type(rval) == dict:
#                 message.update(rval)
#             else:
#                 message['global_merge_vars'] = rval

#             sender_args = {
#                 'template_name': template,
#                 'template_content': [],
#                 'message': message,
#                 'async': True
#             }

#             sender.messages.send_template(**sender_args)

#         return mandrilled

#     return dec


# @mandrillify('resetmcm')
# def password_reset(reset_url):
#     return [{'name': 'reseturl', 'content': reset_url}]


# @mandrillify('confirmmcm')
# def confirmation(activate_url):
#     return [{'name': 'confirmurl', 'content': activate_url}]


# @mandrillify('outdated')
# def mod_outdated(mod_name, mod_url):
#     return [
#         {'name': 'modurl', 'content': mod_url},
#         {'name': 'modname', 'content': mod_name}
#     ]


# @mandrillify('useremail')
# def user_email(sender, message):
#     return {
#         'subject': sender.username + ' on Pack Assembler has sent you a message',
#         'global_merge_vars': [
#             {'name': 'sender', 'content': sender.username},
#             {'name': 'message', 'content': message}
#         ],
#         'headers': {'Reply-To': sender.email}
#     }
