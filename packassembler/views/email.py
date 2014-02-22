from mandrill import Mandrill


def mandrillify(template):

    def dec(f):

        def mandrilled(reg, user, *args, **kwargs):
            sender = Mandrill(reg.settings.get('mandrill_key'))
            message = {
                'to': [{'email': user.email, 'name': user.username}],
                'global_merge_vars': f(*args, **kwargs)
            }

            sender_args = {
                'template_name': template,
                'template_content': [],
                'message': message,
                'async': True
            }

            sender.messages.send_template(**sender_args)

        return mandrilled

    return dec


@mandrillify('resetmcm')
def password_reset(reset_url):
    return [{'name': 'reseturl', 'content': reset_url}]


@mandrillify('confirmmcm')
def confirmation(activate_url):
    return [{'name': 'confirmurl', 'content': activate_url}]


@mandrillify('outdated')
def mod_outdated(mod_name, mod_url):
    return [
        {'name': 'modurl', 'content': mod_url},
        {'name': 'modname', 'content': mod_name}
    ]
