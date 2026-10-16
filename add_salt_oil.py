import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 确保盐和食用油都在
salt, _ = Ingredient.objects.get_or_create(name='盐', defaults={'category': 'seasoning'})
oil, _ = Ingredient.objects.get_or_create(name='食用油', defaults={'category': 'seasoning'})

print("给所有菜谱加上盐和食用油...")
added = 0
for recipe in Recipe.objects.all():
    # 加盐
    if not RecipeIngredient.objects.filter(recipe=recipe, ingredient=salt).exists():
        RecipeIngredient.objects.create(recipe=recipe, ingredient=salt, amount='适量')
        added += 1
    # 加食用油
    if not RecipeIngredient.objects.filter(recipe=recipe, ingredient=oil).exists():
        RecipeIngredient.objects.create(recipe=recipe, ingredient=oil, amount='适量')
        added += 1

print(f"给所有菜谱加了 {added} 个基本食材")
print(f"现在菜谱总数: {Recipe.objects.count()} 道")
print(f"食材总数: {Ingredient.objects.count()} 种")
print(f"关联总数: {RecipeIngredient.objects.count()} 条")

# 测试
print("\n=== 测试 ===")
salt_count = RecipeIngredient.objects.filter(ingredient=salt).count()
oil_count = RecipeIngredient.objects.filter(ingredient=oil).count()
print(f"盐出现在 {salt_count} 道菜里")
print(f"食用油出现在 {oil_count} 道菜里")
