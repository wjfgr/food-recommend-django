import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 确保基本食材都在
basic_ings = [
    ('盐', 'seasoning'),
    ('葱', 'veg'),
    ('姜', 'veg'),
    ('蒜', 'veg'),
    ('食用油', 'seasoning'),
]

print("确保基本食材都在...")
for name, cat in basic_ings:
    ing, created = Ingredient.objects.get_or_create(name=name, defaults={'category': cat})
    if created:
        print(f"  添加: {name}")

# 给所有菜谱都加上这些基本食材
print("\n给所有菜谱配上基本食材...")
added = 0
for recipe in Recipe.objects.all():
    for name in ['盐', '葱', '姜', '蒜', '食用油']:
        ing = Ingredient.objects.filter(name=name).first()
        if not ing:
            continue
        if not RecipeIngredient.objects.filter(recipe=recipe, ingredient=ing).exists():
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ing, amount='适量')
            added += 1

print(f"给所有菜谱加了 {added} 个基本食材")

# 测试常见组合
print("\n=== 测试常见组合 ===")
test_cases = [
    ('盐', '葱'),
    ('盐', '鸡蛋'),
    ('鸡蛋', '葱'),
    ('盐', '猪肉'),
    ('猪肉', '葱'),
]

for ing1_name, ing2_name in test_cases:
    ing1 = Ingredient.objects.filter(name=ing1_name).first()
    ing2 = Ingredient.objects.filter(name=ing2_name).first()
    if not ing1 or not ing2:
        print(f"{ing1_name}+{ing2_name}: 食材不存在")
        continue
    
    recipes = Recipe.objects.filter(
        recipeingredient__ingredient=ing1
    ).filter(
        recipeingredient__ingredient=ing2
    ).distinct()
    
    print(f"{ing1_name}+{ing2_name}: {recipes.count()} 道菜")

print(f"\n现在菜谱总数: {Recipe.objects.count()} 道")
print(f"食材总数: {Ingredient.objects.count()} 种")
print(f"关联总数: {RecipeIngredient.objects.count()} 条")
