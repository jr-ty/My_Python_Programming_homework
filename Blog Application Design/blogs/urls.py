from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    # 新建文章
    path('new_post/', views.new_post, name='new_post'),
    # 编辑文章
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    # 删除路由
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]