from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'email', 'role',)
    list_filter = ('username', 'email',)
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'CustomFields',
            {
                'fields': (
                    'role',
                    'email',
                )
            }

        )
    )

    fieldsets = (*UserAdmin.fieldsets, ('CustomFields', {'fields': ('role', )}))


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'author', ]
