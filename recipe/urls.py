from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('match/', views.match_recipes, name='match'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:pk>/favorite/', views.favorite_toggle, name='favorite_toggle'),
    path('recipes/<int:pk>/rating/', views.rating_add, name='rating_add'),
    path('recipes/<int:pk>/comment/', views.comment_add, name='comment_add'),
    path('search/', views.search, name='search'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('stats/', views.stats, name='stats'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add/', views.add_recipe, name='add_recipe'),
]
