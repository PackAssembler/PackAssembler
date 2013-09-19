from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound
from mcmanager.views.common import NoPermission
from .schema import DoesNotExist


def exception_tween_factory(handler, registry):
    def exception_tween(request):
        try:
            return handler(request)
        except DoesNotExist:
            return HTTPNotFound()
        except NoPermission:
            return HTTPForbidden()
    return exception_tween
