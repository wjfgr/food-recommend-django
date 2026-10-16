import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from recipe.models import Recipe

# 关键词规则
soup_keywords = ['汤', '羹', '煲', '炖']
staple_keywords = ['饭', '面', '粥', '饼', '馒头', '包子', '饺子', '馄饨', '意面', '焗饭', '炒面', '炒饭']
cold_keywords = ['凉拌', '凉', '拌', '卤']

count_soup = 0
count_staple = 0
count_cold = 0

for recipe in Recipe.objects.all():
    name = recipe.name
    
    # 汤羹
    if any(k in name for k in soup_keywords):
        recipe.category = 'soup'
        recipe.save()
        count_soup += 1
    # 主食
    elif any(k in name for k in staple_keywords):
        recipe.category = 'staple'
        recipe.save()
        count_staple += 1
    # 凉菜
    elif any(k in name for k in cold_keywords):
        recipe.category = 'cold'
        recipe.save()
        count_cold += 1

print(f'分类完成！')
print(f'  汤羹: {count_soup} 道')
print(f'  主食: {count_staple} 道')
print(f'  凉菜: {count_cold} 道')
print()

# 重新统计
print('=== 现在各分类数量 ===')
for key, name in Recipe.CATEGORY_CHOICES:
    count = Recipe.objects.filter(category=key).count()
    print(f'  {name}: {count} 道')
