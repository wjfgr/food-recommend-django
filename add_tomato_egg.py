import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from recipe.models import Recipe, Ingredient, RecipeIngredient

# 1. 加食用油食材
oil, created = Ingredient.objects.get_or_create(
    name='食用油',
    defaults={'category': 'seasoning'}
)
status = '新建' if created else '已存在'
print(f'食用油: {status} (id={oil.id})')

# 2. 创建番茄炒蛋菜谱
recipe, created = Recipe.objects.get_or_create(
    name='番茄炒蛋',
    defaults={
        'category': 'home',
        'steps': '''1. 番茄洗净切块，鸡蛋打散加少许盐搅匀
2. 锅中倒油烧热，倒入鸡蛋液炒至凝固盛出
3. 锅中再加少许油，放入番茄块翻炒出汁
4. 加少许糖和盐调味
5. 倒入炒好的鸡蛋翻炒均匀
6. 撒上葱花即可出锅'''
    }
)
status = '新建' if created else '已存在'
print(f'番茄炒蛋: {status} (id={recipe.id})')

# 3. 添加食材关联
ingredients_map = {
    '番茄': '150克',
    '鸡蛋': '3个',
    '葱': '10克',
    '盐': '5克',
    '食用油': '20克',
}

for ing_name, amount in ingredients_map.items():
    ing = Ingredient.objects.filter(name=ing_name).first()
    if ing:
        ri, ri_created = RecipeIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=ing,
            defaults={'amount': amount}
        )
        status = '关联成功' if ri_created else '已关联'
        print(f'  {ing_name}: {status} ({amount})')

print()
print(f'完成！现在总共有 {Recipe.objects.count()} 道菜')
