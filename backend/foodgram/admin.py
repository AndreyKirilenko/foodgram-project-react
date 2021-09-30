from django.contrib import admin
from .models import Ingredients, Tag, Recipe, Favorite, Shopping_cart


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    # list_filter = ('pub_date',)
    # empty_value_display = ' - нет записи - '


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    prepopulated_fields = {'slug':('name',)}
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    # empty_value_display = ' - нет записи - '

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'image', 'text', 'cooking_time', 'pub_date',) # 'tags' ,'ingredients')
    search_fields = ('name',)
    list_filter = ('pub_date', 'cooking_time')
    date_hierarchy = 'pub_date'
    ordering = ('pub_date',)
    # empty_value_display = ' - нет записи - '


@admin.register(Favorite)
class Favorite(admin.ModelAdmin):
    list_display = ('recipe', 'user', )
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    # empty_value_display = ' - нет записи - '


@admin.register(Shopping_cart)
class Shopping_cart(admin.ModelAdmin):
    list_display = ('recipe', 'user', )
    # search_fields = ('text',)
    # list_filter = ('pub_date',)
    # empty_value_display = ' - нет записи - '