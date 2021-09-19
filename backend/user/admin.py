from django.contrib import admin
from .models import Subscription




@admin.register(Subscription)
class Subscription(admin.ModelAdmin):
    list_display = ('user', 'author', )
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    # empty_value_display = ' - нет записи - '