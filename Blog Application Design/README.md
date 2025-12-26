
# Django Blog Project - 个人博客系统

## 项目简介
这是一个基于 Python Django 框架开发的 Web 博客应用程序。该项目实现了完整的用户认证系统（注册、登录、注销），并具备精细的**对象级权限控制**（Object-level Permissions），确保只有文章的作者本人才有权限编辑或删除自己的文章。

本项目是深圳大学《Python程序设计》课程的实验作业（Experiment 4）。

## 核心功能
* **用户认证系统**：基于 `django.contrib.auth` 实现用户的注册、登录与注销。
* **文章管理 (CRUD)**：用户可以发布新文章，并对已发布的文章进行查看。
* **对象级权限控制**：
    * 文章与特定用户（Owner）绑定。
    * 系统在视图层（Views）和模板层（Templates）进行双重校验。
    * **非作者无法看到“编辑”按钮，直接通过 URL 访问编辑页面会返回 404 错误。**
* **UI 界面优化**：
    * 集成 **Bootstrap 5** 前端框架，实现响应式布局。
    * 使用 **django-crispy-forms** 美化表单显示。
    * 卡片式（Card）布局展示文章列表。

## 技术栈
* **后端**：Python 3.13, Django 5.0
* **前端**：HTML5, CSS3, Bootstrap 5
* **工具**：django-crispy-forms
* **数据库**：SQLite (默认)

## 项目结构
```text
Blog Application Design/
├── blogs/                      # 博客应用主要逻辑 (App)
│   ├── migrations/             # 数据库迁移文件
│   ├── templates/blogs/        # HTML 模板文件
│   ├── models.py               # 数据模型 (BlogPost)
│   ├── views.py                # 视图函数 (含权限校验)
│   └── urls.py                 # 路由配置
├── users/                      # 用户认证应用 (App)
│   ├── templates/registration/ # 登录/注册模板
│   └── views.py                # 注册逻辑
├── ll_project/                 # 项目配置文件
│   ├── settings.py             # 全局配置
│   └── urls.py                 # 全局路由
├── static/                     # 静态文件 (CSS/JS/Images)
├── manage.py                   # 项目管理脚本
└── requirements.txt            # 依赖包列表

```

## 运行指南

1. **进入项目目录**
```bash
cd "Blog Application Design"

```


2. **安装依赖**
```bash
pip install django django-bootstrap5 django-crispy-forms

```


3. **迁移数据库**
```bash
python manage.py migrate

```


4. **启动服务器**
```bash
python manage.py runserver

```
5. **访问项目**

打开浏览器访问：http://127.0.0.1:8000/