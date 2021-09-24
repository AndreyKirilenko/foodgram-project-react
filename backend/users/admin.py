from django.contrib import admin
from .models import Subscription, CustomUser
from django.contrib.auth.admin import UserAdmin


# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'role')

admin.site.register(CustomUser, UserAdmin)

@admin.register(Subscription)
class Subscription(admin.ModelAdmin):
    list_display = ('user', 'author', )
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    # empty_value_display = ' - нет записи - '