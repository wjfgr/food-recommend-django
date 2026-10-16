import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 看看所有调料
print("=== 所有调料 ===")
for ing in Ingredient.objects.filter(category='seasoning').order_by('name'):
    count = RecipeIngredient.objects.filter(ingredient=ing).count()
    print(f"  {ing.name}: {count} 道菜")

# 看看盐在不在
salt = Ingredient.objects.filter(name='盐').first()
if salt:
    print(f"\n盐在数据库里，id={salt.id}")
else:
    print("\n数据库里没有盐！")
