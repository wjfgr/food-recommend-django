import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from recipe.models import Recipe

# 菜名关键词到图片的映射
recipe_image_map = {
    '番茄炒蛋': 'dish-fanqiechaodan.jpg',
    '红烧肉': 'dish-hongshaorou.jpg',
    '清蒸鲈鱼': 'dish-qingzhengyu.jpg',
    '八爪鱼': 'dish-bazhuayu.jpg',
    '银鱼蛋饼': 'dish-yinyudanbing.jpg',
    '蛋炒饭': 'dish-danchaofan.jpg',
}

# 测试匹配
print('=== 测试匹配结果 ===')
count = 0
for recipe in Recipe.objects.all()[:50]:
    for keyword, img in recipe_image_map.items():
        if keyword in recipe.name:
            print(f'  {recipe.name} -> {img}')
            count += 1
            break

print(f'\n前50道菜中，{count}道匹配到了专属图片')
