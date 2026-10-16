import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 常见食材白名单（只保留这些）
common_meat = ['猪肉', '牛肉', '羊肉', '鸡肉', '鸡蛋', '鱼', '虾', '排骨', '五花肉', '鸡胸肉', '鸡腿', '鸡翅', '培根', '火腿', '香肠', '肥牛']
common_veg = ['西红柿', '番茄', '土豆', '胡萝卜', '白菜', '卷心菜', '黄瓜', '茄子', '青椒', '尖椒', '豆角', '四季豆', '蘑菇', '香菇', '木耳', '豆腐', '千张', '葱', '姜', '蒜', '洋葱', '菠菜', '芹菜', '韭菜', '西兰花', '花菜', '莴笋', '竹笋', '南瓜', '冬瓜', '丝瓜', '苦瓜', '玉米', '红薯', '山药', '芋头', '莲藕', '茭白']
common_seasoning = ['盐', '糖', '生抽', '老抽', '醋', '料酒', '蚝油', '淀粉', '花椒', '八角', '桂皮', '香叶', '干辣椒', '胡椒', '番茄酱', '豆瓣酱', '味精', '鸡精', '香油', '辣椒油', '食用油', '黄油', '冰糖', '白糖', '蜂蜜', '面粉']
common_staple = ['米饭', '面条', '馒头', '面包', '吐司', '包子', '饺子', '馄饨', '粥', '饼', '年糕', '粉丝', '粉条']

all_common = set(common_meat + common_veg + common_seasoning + common_staple)

print(f"常见食材: {len(all_common)} 种")

# 删掉不在白名单里的食材
deleted = 0
for ing in Ingredient.objects.all():
    if ing.name not in all_common:
        RecipeIngredient.objects.filter(ingredient=ing).delete()
        ing.delete()
        deleted += 1

print(f"删除了 {deleted} 个不常见食材")

# 现在删掉食材太少的菜谱（少于3个食材的）
recipes_to_delete = []
for recipe in Recipe.objects.all():
    count = RecipeIngredient.objects.filter(recipe=recipe).count()
    if count < 3:
        recipes_to_delete.append(recipe)

for r in recipes_to_delete:
    RecipeIngredient.objects.filter(recipe=r).delete()
    r.delete()

print(f"删除了 {len(recipes_to_delete)} 道菜谱")

# 只保留前200道菜
all_recipes = list(Recipe.objects.all())
if len(all_recipes) > 200:
    for r in all_recipes[200:]:
        RecipeIngredient.objects.filter(recipe=r).delete()
        r.delete()
    print(f"只保留前200道菜")

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

print(f"\n食材列表:")
for ing in Ingredient.objects.all().order_by('category', 'name'):
    print(f"  [{ing.category}] {ing.name}")
