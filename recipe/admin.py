from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Favorite, Rating, Comment


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 5


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'difficulty', 'duration', 'created_at']
    list_filter = ['category', 'difficulty']
    search_fields = ['name']
    inlines = [RecipeIngredientInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'created_at']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'score', 'created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'content', 'created_at']
