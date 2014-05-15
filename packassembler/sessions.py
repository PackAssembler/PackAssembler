from pyramid.session import SignedCookieSessionFactory


def includeme(config):
    session_factory = SignedCookieSessionFactory('signedfactorysek')
    config.set_session_factory(session_factory)
