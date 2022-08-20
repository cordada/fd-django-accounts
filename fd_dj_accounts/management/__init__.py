from django.db import DEFAULT_DB_ALIAS


def get_default_username(check_db: bool = True, database: str = DEFAULT_DB_ALIAS) -> str:
    """
    Try to determine the current system user's username to use as a default.

    :param check_db: If ``True``, requires that the username does not match an
        existing ``auth.User`` (otherwise returns an empty string).
    :param database: The database where the unique check will be performed.
    :returns: The username, or an empty string if no username can be
        determined or the suggested username is already taken.
    """
    # TODO: Implement as closely as possible to
    #  ``django.contrib.auth.management.get_default_username()``.
    return ''  # No username can be determined.
