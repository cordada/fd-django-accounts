from typing import Any

from django.core.exceptions import ImproperlyConfigured


def auth_user_model_swapped_receiver(**kwargs: Any) -> None:
    """Trick necessary to be able to test our app with multiple user models.

    .. note::

        The code is mostly a copy of :func:`django.test.signals.user_model_swapped`.

    .. seealso::

        https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model

    """
    from django.apps import apps

    if kwargs['setting'] == 'AUTH_USER_MODEL':
        apps.clear_cache()
        try:
            from django.contrib.auth import get_user_model

            get_user_model()
        except ImproperlyConfigured:
            # Some tests set an invalid AUTH_USER_MODEL.
            pass
