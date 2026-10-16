import os, django, json, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient, Favorite, Rating, Comment

# 清空数据库
print("清空数据库...")
RecipeIngredient.objects.all().delete()
Recipe.objects.all().delete()
Ingredient.objects.all().delete()
Favorite.objects.all().delete()
Rating.objects.all().delete()
Comment.objects.all().delete()

# 常见食材白名单
common_meat = ['猪肉', '牛肉', '羊肉', '鸡肉', '鸡蛋', '鱼', '虾', '排骨', '五花肉', '鸡胸肉', '鸡腿', '鸡翅', '培根', '火腿', '香肠', '肥牛', '鸭肉', '带鱼', '鲫鱼']
common_veg = ['西红柿', '番茄', '土豆', '胡萝卜', '白菜', '卷心菜', '黄瓜', '茄子', '青椒', '尖椒', '豆角', '四季豆', '蘑菇', '香菇', '木耳', '豆腐', '千张', '葱', '姜', '蒜', '洋葱', '菠菜', '芹菜', '韭菜', '西兰花', '花菜', '莴笋', '竹笋', '南瓜', '冬瓜', '丝瓜', '苦瓜', '玉米', '红薯', '山药', '芋头', '莲藕', '茭白', '生菜', '金针菇', '豆芽']
common_seasoning = ['盐', '糖', '生抽', '老抽', '醋', '料酒', '蚝油', '淀粉', '花椒', '八角', '桂皮', '香叶', '干辣椒', '胡椒', '番茄酱', '豆瓣酱', '味精', '鸡精', '香油', '辣椒油', '食用油', '黄油', '冰糖', '白糖', '蜂蜜', '面粉']
common_staple = ['米饭', '面条', '馒头', '面包', '吐司', '包子', '饺子', '馄饨', '粥', '饼', '年糕', '粉丝', '粉条']

all_common = set(common_meat + common_veg + common_seasoning + common_staple)
print(f"常见食材: {len(all_common)} 种")

def classify(name):
    if name in common_seasoning: return 'seasoning'
    if name in common_staple: return 'staple'
    if name in common_meat: return 'meat'
    return 'veg'

print("读取JSON文件...")
with open('data/tran_dataset_single_0.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_name(raw):
    name = raw.strip()
    name = re.sub(r'【[^】]*】', '', name)
    name = re.sub(r'^[\d\.\s\+\-\~]+', '', name)
    name = re.sub(r'^[\d\.\s]+(克|g|kg|斤|两|勺|个|根|片|瓣|颗|把|条|块|杯|ml|毫升|只|朵|粒|份|包|瓶|罐|节|大|小|半)', '', name)
    name = re.sub(r'[\d\.\s]+(克|g|kg|斤|两|勺|个|根|片|瓣|颗|把|条|块|杯|ml|毫升|只|朵|粒|份|包|瓶|罐|节)$', '', name)
    name = re.sub(r'^(一小勺|一勺|两勺|少许|适量|一点|一些|大|小|半|整|颗|根|片|个|一)', '', name)
    name = re.sub(r'（[^）]*）', '', name)
    name = re.sub(r'\([^)]*\)', '', name)
    name = re.sub(r'[#\*\+\-\~\/\\]', '', name)
    return name.strip()

def parse_recipe(item):
    conv = item['conversation'][0]
    input_text = conv['input']
    output_text = conv['output']
    
    name = input_text.replace('的做法', '').strip()
    name = re.sub(r'[—\-–].*$', '', name)
    name = name.strip()
    
    m = re.search(r"您需要准备以下食材:\n\[(.*?)\]\n按以下方法制作:", output_text, re.DOTALL)
    if not m:
        return None
    
    ingredient_str = m.group(1)
    ingredients = []
    seen = set()
    for part in ingredient_str.split("', '"):
        part = part.strip().strip("'\"[]")
        if not part or part.startswith('【'):
            continue
        ing_name = clean_name(part)
        if not ing_name or len(ing_name) < 2 or len(ing_name) > 6:
            continue
        if ing_name in seen:
            continue
        # 只保留常见食材
        if ing_name not in all_common:
            continue
        seen.add(ing_name)
        ingredients.append(ing_name)
    
    m2 = re.search(r"按以下方法制作:\n\[(.*?)\]$", output_text, re.DOTALL)
    if not m2:
        return None
    
    steps = []
    for part in m2.group(1).split("', '"):
        part = part.strip().strip("'\"[]")
        if part and len(part) > 2:
            steps.append(part)
    
    return name, ingredients, steps

# 导入
added = 0
for i, item in enumerate(data[:3000]):
    if added >= 200:
        break
    
    result = parse_recipe(item)
    if not result:
        continue
    
    name, ingredients, steps = result
    
    if len(name) < 2 or len(name) > 20:
        continue
    if len(ingredients) < 3:
        continue
    if len(steps) < 3:
        continue
    
    if Recipe.objects.filter(name=name).exists():
        continue
    
    recipe = Recipe.objects.create(
        name=name,
        category='home',
        difficulty='简单',
        duration=30,
        description='',
        steps='\n'.join(steps[:8]),
    )
    
    for ing_name in ingredients:
        cat = classify(ing_name)
        ing, _ = Ingredient.objects.get_or_create(name=ing_name, defaults={'category': cat})
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ing, amount='适量')
    
    added += 1
    if added % 50 == 0:
        print(f"已导入 {added} 道...")

print(f"\n完成！导入了 {added} 道菜")
print(f"菜谱总数: {Recipe.objects.count()} 道")
print(f"食材总数: {Ingredient.objects.count()} 种")

count = {}
for ing in Ingredient.objects.all():
    count[ing.category] = count.get(ing.category, 0) + 1
print(f"荤菜: {count.get('meat',0)} 种")
print(f"素菜: {count.get('veg',0)} 种")
print(f"调料: {count.get('seasoning',0)} 种")
print(f"主食: {count.get('staple',0)} 种")
