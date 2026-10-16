# 美食推荐系统（Django）

## 项目简介
基于 Python Django 开发的美食推荐网站，实现美食展示、分类筛选、详情查看、后台数据管理等功能。
前端使用 HTML + CSS + JavaScript，后端使用 Django ORM，数据库采用 SQLite。

## 技术栈
- Python 3.x
- Django
- HTML / CSS / JavaScript
- SQLite

## 主要功能
1. 美食列表展示、按分类筛选
2. 美食详情页，包含食材、做法、图片
3. Django 后台管理，可增删改美食数据
4. 图片资源管理

## 项目结构
recipe_project/
- manage.py          # Django 启动入口
- config/            # 项目配置（settings、urls、wsgi）
- recipe/            # 美食主应用
- cookbook/          # 食谱相关应用
- templates/         # HTML 模板
- static/            # 静态资源（CSS、JS、图片）

## 本地运行
1. 克隆项目：git clone https://github.com/wjfgr/food-recommend-django.git
2. 进入项目目录：cd food-recommend-django
3. 安装依赖：pip install django
4. 数据库迁移：python manage.py migrate
5. 启动项目：python manage.py runserver

浏览器访问 http://127.0.0.1:8000 即可。

## 项目截图
（后续补充运行截图）
