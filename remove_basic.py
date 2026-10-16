import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 找到盐、葱、姜、蒜、食用油这些食材
basic_names = ['盐', '葱', '姜', '蒜', '食用油']

print("删除手动添加的基本食材关联...")
deleted = 0
for name in basic_names:
    ing = Ingredient.objects.filter(name=name).first()
    if ing:
        # 删掉所有和这个食材的关联
        count = RecipeIngredient.objects.filter(ingredient=ing).count()
        RecipeIngredient.objects.filter(ingredient=ing).delete()
        print(f"  {name}: 删除了 {count} 个关联")
        deleted += count

print(f"\n总共删除了 {deleted} 个手动添加的关联")

# 现在删掉那些食材太少的菜谱
print("\n删除食材太少的菜谱...")
recipe_deleted = 0
for recipe in Recipe.objects.all():
    count = RecipeIngredient.objects.filter(recipe=recipe).count()
    if count < 3:
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        recipe.delete()
        recipe_deleted += 1

print(f"删除了 {recipe_deleted} 道菜")
print(f"现在菜谱总数: {Recipe.objects.count()} 道")
print(f"食材总数: {Ingredient.objects.count()} 种")
print(f"关联总数: {RecipeIngredient.objects.count()} 条")
