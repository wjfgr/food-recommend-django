import os, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient, Recipe, RecipeIngredient

print("=== 彻底清理食材名 ===")

# 要删除的：标签、带用量的、太长的
to_delete = []
to_rename = {}

for ing in Ingredient.objects.all():
    name = ing.name
    
    # 1. 带#号的标签
    if '#' in name or '【' in name or '】' in name:
        to_delete.append(ing)
        continue
    
    # 2. 带数字开头的（带用量的）
    if re.match(r'^[\d\.\s+]', name):
        to_delete.append(ing)
        continue
    
    # 3. 太长的（超过8个字）
    if len(name) > 8:
        to_delete.append(ing)
        continue
    
    # 4. 清理食材名
    new_name = name
    # 去掉所有数字和单位
    new_name = re.sub(r'\d+[\d\.\s]*(克|g|kg|斤|两|勺|个|根|片|瓣|颗|把|条|块|杯|ml|毫升|只|朵|粒|份|包|瓶|罐|节|适量|少许|大|小|半)', '', new_name)
    new_name = re.sub(r'^[\d\.\s]+', '', new_name)
    new_name = re.sub(r'[\d\.\s]+$', '', new_name)
    new_name = new_name.strip()
    
    if new_name != name and new_name:
        to_rename[ing] = new_name

print(f"要删除: {len(to_delete)} 个")
print(f"要重命名: {len(to_rename)} 个")

# 执行删除
for ing in to_delete:
    RecipeIngredient.objects.filter(ingredient=ing).delete()
    ing.delete()

# 执行重命名
for ing, new_name in to_rename.items():
    # 检查有没有重名
    existing = Ingredient.objects.filter(name=new_name).exclude(id=ing.id).first()
    if existing:
        # 合并到existing
        RecipeIngredient.objects.filter(ingredient=ing).update(ingredient=existing)
        ing.delete()
    else:
        ing.name = new_name
        ing.save()

# 重新分类
def classify(name):
    # 调料
    seasoning_words = ['盐', '糖', '生抽', '老抽', '酱油', '醋', '料酒', '蚝油', '淀粉', '葱', '姜', '蒜', '花椒', '八角', '桂皮', '香叶', '干辣椒', '胡椒', '番茄酱', '豆瓣酱', '味精', '鸡精', '香油', '辣椒油', '芝麻油', '橄榄油', '食用油', '黄油', '冰糖', '白糖', '蜂蜜', '啤酒', '牛奶', '面粉', '淀粉', '泡打粉', '苏打粉']
    for w in seasoning_words:
        if w in name:
            return 'seasoning'
    
    # 主食
    staple_words = ['米饭', '面条', '馒头', '面包', '吐司', '包子', '饺子', '馄饨', '粥', '饼', '年糕', '粽子', '月饼', '面条', '意面', '通心粉']
    for w in staple_words:
        if w in name:
            return 'staple'
    
    # 荤菜
    meat_words = ['猪肉', '牛肉', '羊肉', '鸡肉', '鸭肉', '鸡蛋', '鱼', '虾', '蟹', '排骨', '五花肉', '肉丝', '肉片', '肉末', '肉馅', '牛排', '鸡排', '鸡腿', '鸡翅', '鸭翅', '金枪鱼', '培根', '火腿', '香肠', '腊肉', '午餐肉', '肉丸', '鱼丸', '鸡小腿', '童子鸡', '三黄鸡']
    for w in meat_words:
        if w in name:
            return 'meat'
    
    return 'veg'

for ing in Ingredient.objects.all():
    ing.category = classify(ing.name)
    ing.save()

# 统计
count = {}
for ing in Ingredient.objects.all():
    count[ing.category] = count.get(ing.category, 0) + 1

print(f"\n=== 清理完成 ===")
print(f"食材总数: {Ingredient.objects.count()} 种")
print(f"荤菜: {count.get('meat',0)} 种")
print(f"素菜: {count.get('veg',0)} 种")
print(f"调料: {count.get('seasoning',0)} 种")
print(f"主食: {count.get('staple',0)} 种")

print(f"\n素菜前20:")
for ing in Ingredient.objects.filter(category='veg')[:20]:
    print(f"  {ing.name}")
