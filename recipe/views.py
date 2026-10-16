from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Ingredient, Recipe, RecipeIngredient, Favorite, Rating, Comment
import json

# 菜品图片映射表（70道常见菜专属图）
RECIPE_IMAGE_MAP = {
    # 荤菜
    '番茄炒蛋': 'dish-fanqiechaodan.jpg',
    '红烧肉': 'dish-hongshaorou.jpg',
    '清蒸鲈鱼': 'dish-qingzhengyu.jpg',
    '八爪鱼': 'dish-bazhuayu.jpg',
    '银鱼蛋饼': 'dish-yinyudanbing.jpg',
    '可乐鸡翅': 'dish-kelejichi.jpg',
    '可乐鸡腿': 'dish-kelejitui.jpg',
    '宫保鸡丁': 'dish-gongbaojiding.jpg',
    '糖醋排骨': 'dish-tangupigugu.jpg',
    '鱼香肉丝': 'dish-yuxiangrousi.jpg',
    '红烧排骨': 'dish-hongshaopaigu.jpg',
    '青椒肉丝': 'dish-qingjiaorousi.jpg',
    '炒肉丝': 'dish-chaorousi.jpg',
    '回锅肉': 'dish-huiguorou.jpg',
    '水煮鱼': 'dish-shuizhuyu.jpg',
    '糖醋里脊': 'dish-tanguliji.jpg',
    '木须肉': 'dish-muxurou.jpg',
    '红烧鱼': 'dish-hongshaoyu.jpg',
    '炖牛肉': 'dish-doungrou.jpg',
    '清蒸鸡': 'dish-qingzhengji.jpg',
    '蒜蓉粉丝蒸虾': 'dish-zhengxia.jpg',
    '西红柿炖牛腩': 'dish-fanqieduniunan.jpg',
    '辣子鸡': 'dish-laziji.jpg',
    '水煮肉片': 'dish-shuizhuroupian.jpg',
    '酸菜鱼': 'dish-suancaiyu.jpg',
    '梅菜扣肉': 'dish-meicaikourou.jpg',
    '粉蒸肉': 'dish-fenzhenrou.jpg',
    '烤鸡翅': 'dish-kaojichi.jpg',
    '炸鸡腿': 'dish-zhajitui.jpg',
    '炒鱿鱼': 'dish-chaoyouyu.jpg',
    '番茄龙利鱼': 'dish-fanqiyuli.jpg',
    '土豆炖排骨': 'dish-tudoupaigu.jpg',
    '清蒸虾': 'dish-qingzhengxia.jpg',
    '土豆炖牛肉': 'dish-tudouniurou.jpg',
    '清蒸带鱼': 'dish-qingzhengdaiyu.jpg',
    # 素菜
    '麻婆豆腐': 'dish-mapodoufu.jpg',
    '红烧豆腐': 'dish-hongshaodoufu.jpg',
    '土豆丝': 'dish-tudousi.jpg',
    '酸辣土豆丝': 'dish-suanlatudousi.jpg',
    '炒青菜': 'dish-qingcai.jpg',
    '青菜': 'dish-qingcai.jpg',
    '地三鲜': 'dish-disanxian.jpg',
    '干煸豆角': 'dish-ganbiandoujiao.jpg',
    '炒豆角': 'dish-chaodoujiao.jpg',
    '西兰花': 'dish-xilanhua.jpg',
    '蒜蓉西兰花': 'dish-xilanhua.jpg',
    '炒茄子': 'dish-chaoqiezi.jpg',
    '红烧茄子': 'dish-hongshaoqiezi.jpg',
    '醋溜白菜': 'dish-culiubaicai.jpg',
    '香菇青菜': 'dish-xiangguqingcai.jpg',
    '炒藕片': 'dish-chaooupian.jpg',
    '炒木耳': 'dish-chaomuer.jpg',
    '蒜蓉蒸茄子': 'dish-rongsunzengqiezi.jpg',
    '炒白菜': 'dish-chaobaicai.jpg',
    '干煸肉丝': 'dish-ganbiansousi.jpg',
    # 汤/主食
    '西红柿鸡蛋汤': 'dish-xihongshijidan.jpg',
    '番茄鸡蛋汤': 'dish-xihongshijidan.jpg',
    '蒸蛋羹': 'dish-zhengdangeng.jpg',
    '鸡蛋羹': 'dish-zhengdangeng.jpg',
    '煎鸡蛋': 'dish-jianjidan.jpg',
    '蛋炒饭': 'dish-danchaofan.jpg',
    '白米饭': 'dish-mifan.jpg',
    '米饭': 'dish-mifan.jpg',
    '炸酱面': 'dish-zhajiangmian.jpg',
    '小米粥': 'dish-xiaomizhou.jpg',
    '酸菜粉条': 'dish-suancaifenjiao.jpg',
    '饺子': 'dish-jiaozi.jpg',
    '包子': 'dish-baozi.jpg',
    '紫菜蛋花汤': 'dish-zicaidanhuatang.jpg',
    '冬瓜排骨汤': 'dish-dongguapaigutang.jpg',
    # 凉菜
    '拍黄瓜': 'dish-paihuanggua.jpg',
    '皮蛋豆腐': 'dish-pidandoufu.jpg',
    '凉拌木耳': 'dish-liangbanmuer.jpg',
    '糖拌西红柿': 'dish-tangbanxihongshi.jpg',
    '凉拌黄瓜': 'dish-liangbanhuanggua.jpg',
}

def get_recipe_image(recipe):
    """根据菜名匹配对应的图片"""
    # 1. 先匹配专属菜名
    for keyword, img_file in RECIPE_IMAGE_MAP.items():
        if keyword in recipe.name:
            return f'images/{img_file}'
    # 2. 再匹配核心食材关键词（更宽松的匹配，越具体的越靠前）
    name = recipe.name
    if '番茄' in name or '西红柿' in name:
        return 'images/dish-fanqiechaodan.jpg'
    elif '鸡蛋' in name or '蒸蛋' in name or '蛋羹' in name or '煎蛋' in name:
        return 'images/dish-zhengdangeng.jpg'
    elif '鱼' in name:
        return 'images/dish-qingzhengyu.jpg'
    elif '红烧肉' in name or '红烧排骨' in name:
        return 'images/dish-hongshaorou.jpg'
    elif '鸡' in name and '翅' in name:
        return 'images/dish-kelejichi.jpg'
    elif '鸡' in name:
        return 'images/dish-gongbaojiding.jpg'
    elif '排骨' in name:
        return 'images/dish-tangupigugu.jpg'
    elif '豆腐' in name:
        return 'images/dish-mapodoufu.jpg'
    elif '土豆' in name:
        return 'images/dish-tudousi.jpg'
    elif '青菜' in name or '白菜' in name:
        return 'images/dish-qingcai.jpg'
    elif '面' in name:
        return 'images/dish-zhajiangmian.jpg'
    elif '粥' in name:
        return 'images/dish-xiaomizhou.jpg'
    elif '饺子' in name:
        return 'images/dish-jiaozi.jpg'
    elif '包子' in name:
        return 'images/dish-baozi.jpg'
    elif '米饭' in name or '炒饭' in name:
        return 'images/dish-mifan.jpg'
    # 3. 最后按分类返回通用图
    if recipe.category == 'soup':
        return 'images/dish-soup.jpg'
    elif recipe.category == 'staple':
        return 'images/dish-staple.jpg'
    elif recipe.category == 'cold':
        return 'images/dish-cold.jpg'
    else:
        return 'images/dish-veg.jpg'




def home(request):
    ingredients = Ingredient.objects.all().order_by('category', 'name')
    categories = dict(Ingredient.CATEGORY_CHOICES)
    return render(request, 'recipe/home.html', {
        'ingredients': ingredients, 'categories': categories,
    })


# 食材同义词映射
INGREDIENT_SYNONYMS = {
    '西红柿': ['番茄'],
    '番茄': ['西红柿'],
    '土豆': ['马铃薯'],
    '马铃薯': ['土豆'],
    '鸡蛋': ['鸡子'],
}

def get_all_synonyms(name):
    """获取食材的所有同义词"""
    result = {name}
    if name in INGREDIENT_SYNONYMS:
        result.update(INGREDIENT_SYNONYMS[name])
    return result

def match_recipes(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('ingredients')
        selected_ids = [int(x) for x in selected_ids if x]
        if not selected_ids:
            return render(request, 'recipe/match_result.html', {
                'perfect': [], 'near': [], 'selected': [], 'msg': '请先勾选至少一种食材'
            })
        selected_qs = Ingredient.objects.filter(id__in=selected_ids)
        selected_names = set(selected_qs.values_list('name', flat=True))
        # 扩展同义词
        expanded_names = set()
        for name in selected_names:
            expanded_names.update(get_all_synonyms(name))
        selected_names = expanded_names
        # 基础调料，默认都有，不算缺失
        BASIC_SEASONINGS = {'盐', '食用油', '油', '葱', '姜', '蒜', '酱油', '生抽', '老抽', '糖', '料酒', '胡椒粉', '花椒'}
        
        perfect, near = [], []
        for recipe in Recipe.objects.all():
            needed = set(recipe.ingredients.values_list('name', flat=True))
            if not needed:
                continue
            have = needed & selected_names
            # 缺失的食材里，去掉基础调料
            missing = (needed - selected_names) - BASIC_SEASONINGS
            ratio = len(have) / len(needed) if needed else 0
            if len(have) == 0:
                continue
            if len(selected_names) == 1:
                near.append({'recipe': recipe, 'ratio': ratio, 'missing': sorted(missing)})
            elif len(missing) == 0:
                perfect.append({'recipe': recipe, 'ratio': ratio, 'missing': []})
            elif len(missing) <= 2:
                near.append({'recipe': recipe, 'ratio': ratio, 'missing': sorted(missing)})
        
        def sort_key(item):
            recipe = item['recipe']
            name_match = 1 if any(ing_name in recipe.name for ing_name in selected_names) else 0
            return (-name_match, -item['ratio'], len(item['missing']))
        
        perfect.sort(key=sort_key)
        near.sort(key=sort_key)
        # 给每个recipe对象加上image属性
        for item in perfect:
            item['recipe'].image = get_recipe_image(item['recipe'])
        for item in near:
            item['recipe'].image = get_recipe_image(item['recipe'])
        return render(request, 'recipe/match_result.html', {
            'perfect': perfect, 'near': near, 'selected': selected_qs,
        })
    return redirect('home')


def recipe_list(request):
    category = request.GET.get('category', '')
    recipes = list(Recipe.objects.all())
    if category:
        recipes = [r for r in recipes if r.category == category]
    # 给每个recipe对象加上image属性，并标记是否有专属图
    with_image = []
    without_image = []
    for r in recipes:
        r.image = get_recipe_image(r)
        # 判断是否是专属图（不是通用分类图）
        is_custom = False
        for keyword, img_file in RECIPE_IMAGE_MAP.items():
            if keyword in r.name:
                is_custom = True
                break
        if is_custom:
            with_image.append(r)
        else:
            without_image.append(r)
    # 有专属图的排前面
    sorted_recipes = with_image + without_image
    return render(request, 'recipe/list.html', {
        'recipes': sorted_recipes, 'categories': Recipe.CATEGORY_CHOICES, 'current_category': category,
    })


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.image = get_recipe_image(recipe)
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    comments = recipe.comments.all()
    is_favorited = False
    my_rating = None
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
        rating = Rating.objects.filter(user=request.user, recipe=recipe).first()
        my_rating = rating.score if rating else None
    avg_rating = 0
    ratings = Rating.objects.filter(recipe=recipe)
    if ratings.exists():
        avg_rating = sum(r.score for r in ratings) / ratings.count()
    steps_list = [s.strip() for s in recipe.steps.split('\n') if s.strip()]
    return render(request, 'recipe/detail.html', {
        'recipe': recipe, 'recipe_ingredients': recipe_ingredients,
        'comments': comments, 'is_favorited': is_favorited,
        'my_rating': my_rating, 'avg_rating': round(avg_rating, 1),
        'steps': steps_list,
    })


@login_required
def favorite_toggle(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    fav = Favorite.objects.filter(user=request.user, recipe=recipe).first()
    if fav:
        fav.delete()
    else:
        Favorite.objects.create(user=request.user, recipe=recipe)
    return redirect('recipe_detail', pk=pk)


@login_required
def rating_add(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        score = int(request.POST.get('score', 5))
        Rating.objects.update_or_create(
            user=request.user, recipe=recipe, defaults={'score': score})
    return redirect('recipe_detail', pk=pk)


@login_required
def comment_add(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(user=request.user, recipe=recipe, content=content)
    return redirect('recipe_detail', pk=pk)


def search(request):
    q = request.GET.get('q', '')
    results = list(Recipe.objects.filter(name__icontains=q)) if q else []
    for r in results:
        r.image = get_recipe_image(r)
    return render(request, 'recipe/search.html', {'results': results, 'q': q})


@login_required
def my_favorites(request):
    favs = Favorite.objects.filter(user=request.user).select_related('recipe')
    for fav in favs:
        fav.recipe.image = get_recipe_image(fav.recipe)
    return render(request, 'recipe/favorites.html', {'favorites': favs})


def stats(request):
    top_fav = Recipe.objects.annotate(count=Count('favorite')).order_by('-count')[:5]
    cat_stats = Recipe.objects.values('category').annotate(count=Count('id'))
    categories = dict(Recipe.CATEGORY_CHOICES)
    top_comment = Recipe.objects.annotate(count=Count('comments')).order_by('-count')[:5]
    return render(request, 'recipe/stats.html', {
        'top_fav_json': json.dumps([{'name': r.name, 'count': r.count} for r in top_fav], ensure_ascii=False),
        'cat_labels_json': json.dumps([categories[c['category']] for c in cat_stats], ensure_ascii=False),
        'cat_data_json': json.dumps([c['count'] for c in cat_stats]),
        'top_comment_json': json.dumps([{'name': r.name, 'count': r.count} for r in top_comment], ensure_ascii=False),
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'recipe/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'recipe/login.html', {'form': form})


def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')



@login_required
def add_recipe(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', 'home')
        difficulty = request.POST.get('difficulty', '简单')
        duration = request.POST.get('duration', 15)
        description = request.POST.get('description', '').strip()
        steps = request.POST.get('steps', '').strip()
        
        if not name or not steps:
            return render(request, 'recipe/add_recipe.html', {
                'error': '菜名和做法步骤不能为空',
                'categories': Recipe.CATEGORY_CHOICES,
            })
        
        recipe = Recipe.objects.create(
            name=name,
            category=category,
            difficulty=difficulty,
            duration=duration,
            description=description,
            steps=steps,
        )
        
        # 处理食材
        ing_names = request.POST.getlist('ing_name[]')
        ing_amounts = request.POST.getlist('ing_amount[]')
        for i in range(len(ing_names)):
            ing_name = ing_names[i].strip()
            amount = ing_amounts[i].strip()
            if ing_name:
                ing, created = Ingredient.objects.get_or_create(name=ing_name)
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ing,
                    amount=amount or '适量'
                )
        
        return redirect('recipe_detail', pk=recipe.id)
    
    return render(request, 'recipe/add_recipe.html', {
        'categories': Recipe.CATEGORY_CHOICES,
    })























