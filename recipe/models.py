from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    CATEGORY_CHOICES = [
        ('meat', '荤菜'),
        ('veg', '素菜'),
        ('seasoning', '调料'),
        ('staple', '主食'),
    ]
    name = models.CharField('食材名', max_length=50, unique=True)
    category = models.CharField('分类', max_length=20, choices=CATEGORY_CHOICES, default='veg')

    class Meta:
        verbose_name = '食材'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('home', '家常菜'),
        ('soup', '汤羹'),
        ('staple', '主食'),
        ('cold', '凉菜'),
    ]
    name = models.CharField('菜名', max_length=100)
    category = models.CharField('分类', max_length=20, choices=CATEGORY_CHOICES, default='home')
    difficulty = models.CharField('难度', max_length=20, default='简单')
    duration = models.IntegerField('预计时长(分钟)', default=15)
    description = models.TextField('简介', blank=True)
    steps = models.TextField('做法步骤', help_text='每行一步')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name='所需食材')
    video_url = models.URLField('视频链接', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '菜谱'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField('用量', max_length=50, help_text='如：2个、50g、少许')

    class Meta:
        verbose_name = '菜谱食材'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name} {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='菜谱')
    created_at = models.DateTimeField('收藏时间', auto_now_add=True)

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user.username} 收藏了 {self.recipe.name}'


class Rating(models.Model):
    SCORE_CHOICES = [(i, f'{i}星') for i in range(1, 6)]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='菜谱')
    score = models.IntegerField('评分', choices=SCORE_CHOICES, default=5)
    created_at = models.DateTimeField('评分时间', auto_now_add=True)

    class Meta:
        verbose_name = '评分'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user.username} 给 {self.recipe.name} {self.score}星'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='菜谱', related_name='comments')
    content = models.TextField('评论内容')
    created_at = models.DateTimeField('评论时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} 评论 {self.recipe.name}'