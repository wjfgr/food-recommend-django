import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient, Favorite, Rating, Comment

print("=" * 50)
print("项目数据全面检查")
print("=" * 50)

# 1. 基本统计
print("\n【1. 基本统计】")
print(f"菜谱总数: {Recipe.objects.count()} 道")
print(f"食材总数: {Ingredient.objects.count()} 种")
print(f"关联总数: {RecipeIngredient.objects.count()} 条")
print(f"收藏总数: {Favorite.objects.count()} 条")
print(f"评分总数: {Rating.objects.count()} 条")
print(f"评论总数: {Comment.objects.count()} 条")

# 2. 分类统计
print("\n【2. 食材分类统计】")
count = {}
for ing in Ingredient.objects.all():
    count[ing.category] = count.get(ing.category, 0) + 1
print(f"荤菜: {count.get('meat', 0)} 种")
print(f"素菜: {count.get('veg', 0)} 种")
print(f"调料: {count.get('seasoning', 0)} 种")
print(f"主食: {count.get('staple', 0)} 种")

# 3. 检查问题食材
print("\n【3. 检查问题食材】")
problems = []
for ing in Ingredient.objects.all():
    # 检查食材名长度
    if len(ing.name) < 1 or len(ing.name) > 10:
        problems.append(f"食材名长度异常: {ing.name}")
    # 检查食材名里有没有数字或特殊符号
    if any(c.isdigit() for c in ing.name):
        problems.append(f"食材名里有数字: {ing.name}")
    if any(c in ing.name for c in ['ml', 'g', 'kg', '克', '勺', '个', '根', '片', '瓣']):
        problems.append(f"食材名里有单位: {ing.name}")

if problems:
    print(f"发现 {len(problems)} 个问题:")
    for p in problems[:10]:
        print(f"  - {p}")
else:
    print("没有发现问题食材")

# 4. 检查问题菜谱
print("\n【4. 检查问题菜谱】")
recipe_problems = []
for recipe in Recipe.objects.all():
    ings = RecipeIngredient.objects.filter(recipe=recipe)
    # 食材太少
    if ings.count() < 2:
        recipe_problems.append(f"食材太少({ings.count()}个): {recipe.name}")
    # 步骤太少
    steps = [s for s in recipe.steps.split('\n') if s.strip()]
    if len(steps) < 2:
        recipe_problems.append(f"步骤太少({len(steps)}步): {recipe.name}")
    # 菜名太长或太短
    if len(recipe.name) < 2 or len(recipe.name) > 30:
        recipe_problems.append(f"菜名长度异常({len(recipe.name)}字): {recipe.name}")

if recipe_problems:
    print(f"发现 {len(recipe_problems)} 个问题菜谱:")
    for p in recipe_problems[:10]:
        print(f"  - {p}")
else:
    print("没有发现问题菜谱")

# 5. 检查有没有空食材或空步骤
print("\n【5. 检查空数据】")
empty_ing = Recipe.objects.filter(recipeingredient__isnull=True).distinct().count()
print(f"没有食材的菜谱: {empty_ing} 道")

# 6. 测试常见组合
print("\n【6. 测试常见食材组合】")
test_cases = [
    ('盐', '食用油'),
    ('盐', '鸡蛋'),
    ('鸡蛋', '西红柿'),
    ('盐', '猪肉'),
]

for ing1_name, ing2_name in test_cases:
    ing1 = Ingredient.objects.filter(name=ing1_name).first()
    ing2 = Ingredient.objects.filter(name=ing2_name).first()
    if not ing1 or not ing2:
        print(f"  {ing1_name}+{ing2_name}: 食材不存在")
        continue
    
    recipes = Recipe.objects.filter(
        recipeingredient__ingredient=ing1
    ).filter(
        recipeingredient__ingredient=ing2
    ).distinct()
    
    print(f"  {ing1_name}+{ing2_name}: {recipes.count()} 道菜")

print("\n" + "=" * 50)
print("检查完成!")
print("=" * 50)
