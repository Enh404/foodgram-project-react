from django.contrib import admin

from .models import Tag, Ingredient, Recipe, NumberOfIngredients, Favorite, ShoppingList

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'num_of_favorites')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)

    def num_of_favorites(self, obj):
        return obj.favorites.count()


@admin.register(NumberOfIngredients)
class NumberOfIngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'quantity')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(ShoppingList)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')