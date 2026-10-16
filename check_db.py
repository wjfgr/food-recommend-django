import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 看看数据库里有没有盐
print("=== 数据库里的调料 ===")
for ing in Ingredient.objects.filter(category='seasoning').order_by('name'):
    print(f"  {ing.name}")

# 找一道菜看看它的食材
print("\n=== 随便找3道菜看看食材 ===")
for recipe in Recipe.objects.all()[:3]:
    ings = RecipeIngredient.objects.filter(recipe=recipe)
    print(f"\n菜名: {recipe.name}")
    for ri in ings:
        print(f"  - {ri.ingredient.name}")
