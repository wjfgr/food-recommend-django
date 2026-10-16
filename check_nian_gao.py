import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 找年糕这个食材
nian_gao = Ingredient.objects.filter(name='年糕').first()
if nian_gao:
    print(f"年糕在数据库里")
    # 找所有包含年糕的菜谱
    recipes = Recipe.objects.filter(recipeingredient__ingredient=nian_gao).distinct()
    print(f"包含年糕的菜谱有 {recipes.count()} 道:")
    for r in recipes:
        print(f"  - {r.name}")
else:
    print("数据库里没有年糕！")
