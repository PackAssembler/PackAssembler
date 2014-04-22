from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings,
                          root_factory='packassembler.security.Root')
    config.include(__name__)
    return config.make_wsgi_app()


def includeme(config):
    config.include('.security')
    config.include('.tweens')
    config.include('.routes')
    config.include('.views')
