import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

# 删掉我手动加的那些菜谱
manual_recipes = [
    '土豆烧肉', '白菜炖肉', '红烧肉', '番茄炒蛋', 
    '酸辣土豆丝', '鱼香肉丝', '清蒸鱼', '清炒白菜',
    '青椒肉丝', '西红柿蛋汤'
]

print("删除手动添加的菜谱...")
deleted = 0
for name in manual_recipes:
    r = Recipe.objects.filter(name=name).first()
    if r:
        RecipeIngredient.objects.filter(recipe=r).delete()
        r.delete()
        deleted += 1
        print(f"  删除: {name}")

print(f"\n删除了 {deleted} 道菜")
print(f"现在菜谱总数: {Recipe.objects.count()} 道")
