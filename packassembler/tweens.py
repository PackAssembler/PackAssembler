from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound
from packassembler.views.common import NoPermission
from .schema import DoesNotExist


def includeme(config):
    config.add_tween('packassembler.tweens.exception_tween_factory')


def exception_tween_factory(handler, registry):
    def exception_tween(request):
        try:
            return handler(request)
        except DoesNotExist:
            return HTTPNotFound()
        except NoPermission:
            return HTTPForbidden()
    return exception_tween
