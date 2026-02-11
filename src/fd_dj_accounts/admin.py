from __future__ import annotations

from typing import TYPE_CHECKING

import django.contrib.auth.admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User


if TYPE_CHECKING:
    import django.forms
    import django.http


@admin.register(User)
class UserAdmin(django.contrib.auth.admin.UserAdmin):
    fieldsets = [
        (
            None,
            {
                'fields': [
                    django.contrib.auth.get_user_model().USERNAME_FIELD,
                    'password',
                ],
            },
        ),
        (
            _('Personal info'),
            {
                'fields': [
                    # django.contrib.auth.get_user_model().get_email_field_name(),
                ],
            },
        ),
        (
            _('Permissions'),
            {
                'fields': [
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ],
            },
        ),
        (
            _('Important dates'),
            {
                'fields': [
                    'last_login',
                    'created_at',
                    'deactivated_at',
                ],
            },
        ),
    ]

    add_fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': [
                    django.contrib.auth.get_user_model().USERNAME_FIELD,
                    'password1',
                    'password2',
                ],
            },
        ),
    ]

    list_display = [
        django.contrib.auth.get_user_model().USERNAME_FIELD,
        # django.contrib.auth.get_user_model().get_email_field_name(),
        'is_staff',
    ]

    list_filter = [
        'is_staff',
        'is_superuser',
        'is_active',
    ]

    search_fields = [
        django.contrib.auth.get_user_model().USERNAME_FIELD,
        # django.contrib.auth.get_user_model().get_email_field_name(),
    ]

    ordering = [
        django.contrib.auth.get_user_model().USERNAME_FIELD,
    ]

    filter_horizontal = []  # type: ignore[var-annotated]

    def save_model(
        self,
        request: django.http.HttpRequest,
        obj: User,
        form: django.forms.ModelForm,
        change: bool,
    ) -> None:
        if change:
            pass
        else:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)
