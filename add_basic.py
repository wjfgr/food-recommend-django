import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 最基本的食材，确保都有
basic_ingredients = [
    ('盐', 'seasoning'),
    ('醋', 'seasoning'),
    ('葱', 'veg'),
    ('姜', 'veg'),
    ('蒜', 'veg'),
    ('食用油', 'seasoning'),
]

print("添加基本食材...")
for name, cat in basic_ingredients:
    ing, created = Ingredient.objects.get_or_create(name=name, defaults={'category': cat})
    if created:
        print(f"  添加: {name}")

# 给所有菜谱都加上盐、葱、姜、蒜（每道菜都要用）
print("\n给所有菜谱配上基本调料...")
added = 0
for recipe in Recipe.objects.all():
    for name in ['盐', '葱', '姜', '蒜']:
        ing = Ingredient.objects.filter(name=name).first()
        if not ing:
            continue
        # 检查这道菜里有没有这个食材
        if not RecipeIngredient.objects.filter(recipe=recipe, ingredient=ing).exists():
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ing, amount='适量')
            added += 1

print(f"给所有菜谱加了 {added} 个基本食材")

# 统计
print(f"\n=== 最终结果 ===")
print(f"菜谱: {Recipe.objects.count()} 道")
print(f"食材: {Ingredient.objects.count()} 种")
print(f"关联: {RecipeIngredient.objects.count()} 条")

count = {}
for ing in Ingredient.objects.all():
    count[ing.category] = count.get(ing.category, 0) + 1
print(f"荤菜: {count.get('meat',0)} 种")
print(f"素菜: {count.get('veg',0)} 种")
print(f"调料: {count.get('seasoning',0)} 种")
print(f"主食: {count.get('staple',0)} 种")
