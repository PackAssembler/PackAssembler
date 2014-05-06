from pyramid.request import Request
from pyramid.config import Configurator


class CustomRequest(Request):
    def flash(self, msg):
        self.session.flash(msg)

    def flash_error(self, msg):
        self.session.flash(msg, 'errors')


def main(global_config, **settings):
    config = Configurator(settings=settings, request_factory=CustomRequest)
    config.include(__name__)
    return config.make_wsgi_app()


def includeme(config):
    config.include('.security')
    config.include('.tweens')
    config.include('.routes')
    config.include('.views')
    config.include('.sessions')
