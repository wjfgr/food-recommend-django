import os, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 常见食材白名单
common_meat = ['猪肉', '牛肉', '羊肉', '鸡肉', '鸡蛋', '鱼', '虾', '排骨', '五花肉', '鸡胸肉', '鸡腿', '鸡翅', '培根', '火腿', '香肠', '肥牛', '鸭肉', '带鱼', '鲫鱼']
common_veg = ['西红柿', '番茄', '土豆', '胡萝卜', '白菜', '卷心菜', '黄瓜', '茄子', '青椒', '尖椒', '豆角', '四季豆', '蘑菇', '香菇', '木耳', '豆腐', '千张', '葱', '姜', '蒜', '洋葱', '菠菜', '芹菜', '韭菜', '西兰花', '花菜', '莴笋', '竹笋', '南瓜', '冬瓜', '丝瓜', '苦瓜', '玉米', '红薯', '山药', '芋头', '莲藕', '茭白', '生菜', '金针菇', '豆芽']
common_seasoning = ['盐', '糖', '生抽', '老抽', '醋', '料酒', '蚝油', '淀粉', '花椒', '八角', '桂皮', '香叶', '干辣椒', '胡椒', '番茄酱', '豆瓣酱', '味精', '鸡精', '香油', '辣椒油', '食用油', '黄油', '冰糖', '白糖', '蜂蜜', '面粉']
common_staple = ['米饭', '面条', '馒头', '面包', '吐司', '包子', '饺子', '馄饨', '粥', '饼', '年糕', '粉丝', '粉条']

all_common = set(common_meat + common_veg + common_seasoning + common_staple)

def classify(name):
    if name in common_seasoning: return 'seasoning'
    if name in common_staple: return 'staple'
    if name in common_meat: return 'meat'
    return 'veg'

print("从做法步骤里提取食材，补到食材列表...")
added = 0

for recipe in Recipe.objects.all():
    steps = recipe.steps
    
    # 检查每个常见食材是否在步骤里提到
    for ing_name in all_common:
        if ing_name in steps:
            # 检查这道菜里有没有这个食材
            existing = RecipeIngredient.objects.filter(
                recipe=recipe, 
                ingredient__name=ing_name
            ).exists()
            
            if not existing:
                # 加上这个食材
                ing, _ = Ingredient.objects.get_or_create(name=ing_name, defaults={'category': classify(ing_name)})
                RecipeIngredient.objects.create(recipe=recipe, ingredient=ing, amount='适量')
                added += 1

print(f"从步骤里补充了 {added} 个食材")
print(f"现在菜谱总数: {Recipe.objects.count()} 道")
print(f"食材总数: {Ingredient.objects.count()} 种")
print(f"关联总数: {RecipeIngredient.objects.count()} 条")
