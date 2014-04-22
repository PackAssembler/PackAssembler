import re


def linejoin(text):
    try:
        return '<br />'.join(text.splitlines())
    except AttributeError:
        return 'None'


def externallink(text):
    trun = text[:35] + (text[35:] and '...')
    return '<a href="{0}" rel="nofollow">{1}</a>'.format(text, trun)


def autolink(text):
    urlre = re.compile('(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
    try:
        return urlre.sub(lambda m: externallink(m.group(0)), text)
    except TypeError:
        return 'None'