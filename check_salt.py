import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 看看数据库里有没有盐
salt = Ingredient.objects.filter(name='盐').first()
if salt:
    count = RecipeIngredient.objects.filter(ingredient=salt).count()
    print(f"盐在数据库里，出现在 {count} 道菜里")
else:
    print("数据库里没有盐！")

# 看看数据库里的调料
print("\n=== 数据库里的调料 ===")
for ing in Ingredient.objects.filter(category='seasoning').order_by('name'):
    count = RecipeIngredient.objects.filter(ingredient=ing).count()
    print(f"  {ing.name}: {count} 道菜")
