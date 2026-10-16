import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 找出那些食材太少的菜谱（少于4个食材的）
print("找出食材太少的菜谱...")
bad_recipes = []
for recipe in Recipe.objects.all():
    count = RecipeIngredient.objects.filter(recipe=recipe).count()
    if count < 4:
        bad_recipes.append((recipe.name, count))

print(f"发现 {len(bad_recipes)} 道食材太少的菜谱:")
for name, count in bad_recipes[:20]:
    print(f"  {name}: {count} 个食材")

# 删掉这些奇怪的菜谱
print("\n删除这些奇怪的菜谱...")
deleted = 0
for recipe in Recipe.objects.all():
    count = RecipeIngredient.objects.filter(recipe=recipe).count()
    if count < 4:
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        recipe.delete()
        deleted += 1

print(f"删除了 {deleted} 道菜")
print(f"现在菜谱总数: {Recipe.objects.count()} 道")
