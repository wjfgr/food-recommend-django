import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

def get_ing(name):
    ing, _ = Ingredient.objects.get_or_create(name=name, defaults={'category': 'veg'})
    return ing

# 最常见的家常菜，确保常见组合都能匹配
common_recipes = [
    {
        'name': '土豆烧肉',
        'steps': '猪肉切块焯水\n土豆切块\n锅里放油炒糖色\n下猪肉翻炒上色\n加生抽老抽料酒\n加水炖30分钟\n加土豆再炖15分钟\n大火收汁',
        'ingredients': ['猪肉', '土豆', '生抽', '老抽', '料酒', '冰糖', '葱', '姜', '蒜', '盐']
    },
    {
        'name': '白菜炖肉',
        'steps': '猪肉切片\n白菜切段\n锅里放油炒肉片\n加白菜翻炒\n加水炖15分钟\n加盐调味',
        'ingredients': ['猪肉', '白菜', '盐', '葱', '姜', '蒜']
    },
    {
        'name': '红烧肉',
        'steps': '五花肉切块焯水\n锅里放冰糖炒糖色\n下五花肉翻炒上色\n加生抽老抽料酒\n加水炖40分钟\n大火收汁',
        'ingredients': ['五花肉', '冰糖', '生抽', '老抽', '料酒', '葱', '姜', '盐']
    },
    {
        'name': '番茄炒蛋',
        'steps': '西红柿切块\n鸡蛋打散\n锅里倒油炒鸡蛋盛出\n再倒油炒西红柿\n加糖加盐\n倒鸡蛋翻炒均匀',
        'ingredients': ['西红柿', '鸡蛋', '白糖', '盐', '葱']
    },
    {
        'name': '酸辣土豆丝',
        'steps': '土豆切丝\n泡水里去淀粉\n锅里倒油爆香花椒干辣椒\n下土豆丝翻炒\n加醋加盐\n炒至断生出锅',
        'ingredients': ['土豆', '青椒', '干辣椒', '花椒', '醋', '盐', '葱']
    },
    {
        'name': '鱼香肉丝',
        'steps': '猪肉切丝\n加料酒淀粉腌制\n木耳胡萝卜切丝\n调鱼香汁：醋糖生抽淀粉水\n锅里倒油炒肉丝盛出\n炒蔬菜丝\n倒肉丝和鱼香汁翻炒',
        'ingredients': ['猪肉', '木耳', '胡萝卜', '青椒', '醋', '白糖', '生抽', '淀粉']
    },
    {
        'name': '清蒸鱼',
        'steps': '鱼处理干净\n身上划几刀\n放姜片葱段\n水开后蒸10分钟\n倒掉蒸出的水\n淋生抽热油\n放葱丝',
        'ingredients': ['鲫鱼', '姜', '葱', '生抽', '食用油', '盐']
    },
    {
        'name': '清炒白菜',
        'steps': '白菜切段\n锅里倒油爆香蒜末\n下白菜翻炒\n加盐\n炒至变软出锅',
        'ingredients': ['白菜', '蒜', '盐', '食用油']
    },
    {
        'name': '青椒肉丝',
        'steps': '猪肉切丝\n加料酒淀粉腌制\n青椒切丝\n锅里倒油炒肉丝盛出\n炒青椒丝\n倒肉丝翻炒加盐',
        'ingredients': ['猪肉', '青椒', '料酒', '淀粉', '盐', '葱']
    },
    {
        'name': '西红柿蛋汤',
        'steps': '西红柿切块\n锅里放水烧开\n下西红柿煮5分钟\n鸡蛋打散淋入\n加盐香油\n撒葱花',
        'ingredients': ['西红柿', '鸡蛋', '盐', '葱', '香油']
    },
]

print("补充常见家常菜...")
added = 0
for r_data in common_recipes:
    if Recipe.objects.filter(name=r_data['name']).exists():
        continue
    
    recipe = Recipe.objects.create(
        name=r_data['name'],
        category='home',
        difficulty='简单',
        duration=20,
        description='',
        steps=r_data['steps'],
    )
    
    for ing_name in r_data['ingredients']:
        ing = get_ing(ing_name)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ing, amount='适量')
    
    added += 1
    print(f"  添加: {r_data['name']}")

print(f"\n完成！补充了 {added} 道菜")
print(f"现在菜谱总数: {Recipe.objects.count()} 道")

# 重新测试
print("\n=== 重新测试 ===")
test_cases = [
    ('猪肉', '鸡蛋'),
    ('鸡蛋', '西红柿'),
    ('猪肉', '土豆'),
    ('鸡蛋', '葱'),
    ('猪肉', '白菜'),
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
