from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, Shopping_cart, Tag


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'image', 'text', 'cooking_time', 'pub_date'
    )
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    date_hierarchy = 'pub_date'
    ordering = ('pub_date',)


@admin.register(Favorite)
class Favorite(admin.ModelAdmin):
    list_display = ('recipe', 'user', )


@admin.register(Shopping_cart)
class Shopping_cart(admin.ModelAdmin):
    list_display = ('recipe', 'user', )
