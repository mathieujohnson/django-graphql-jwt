from functools import wraps

from django.utils.translation import gettext as _

from .. import exceptions
from ..utils import get_cookie_name


def ensure_refresh_token(f):
    @wraps(f)
    def wrapper(cls, root, info, refresh_token=None, *args, **kwargs):
        if refresh_token is None:
            refresh_token = info.context.COOKIES.get(
                get_cookie_name(info.context, True),
            )
            if refresh_token is None:
                raise exceptions.JSONWebTokenError(
                    _('Refresh token is required'),
                )
        return f(cls, root, info, refresh_token, *args, **kwargs)
    return wrapper
