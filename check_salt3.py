import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from recipe.models import Ingredient

salt = Ingredient.objects.filter(name='盐').first()
if salt:
    print(f"盐: name={salt.name}, category={salt.category}")
    
# 看看所有seasoning分类的食材
print("\n=== seasoning分类的食材 ===")
for ing in Ingredient.objects.filter(category='seasoning').order_by('name'):
    print(f"  {ing.name}")
