from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404 # 用于抛出404错误
from django.core.paginator import Paginator # 引入分页器

from .models import BlogPost
from .forms import BlogPostForm

def index(request):
    """主页：显示所有文章，带分页"""
    posts_list = BlogPost.objects.order_by('-date_added')

    # 每页显示 6 篇文章
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 判断是否需要显示分页条
    is_paginated = page_obj.has_other_pages()

    context = {
        'posts': page_obj, # 注意这里传的是 page_obj 而不是 posts_list
        'page_obj': page_obj,
        'is_paginated': is_paginated
    }
    return render(request, 'blogs/index.html', context)

@login_required
def new_post(request):
    """添加新文章"""
    if request.method != 'POST':
        form = BlogPostForm()
    else:
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            # 关键步骤：不立即保存到数据库
            new_post = form.save(commit=False)
            # 19-5: 将当前登录用户设为所有者
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:index')

    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """编辑文章"""
    post = get_object_or_404(BlogPost, id=post_id)

    # 19-5: 核心保护逻辑
    # 检查当前用户是否是文章所有者
    if post.owner != request.user:
        raise Http404("你没有权限编辑此文章。")

    if request.method != 'POST':
        form = BlogPostForm(instance=post)
    else:
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')

    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)


@login_required
def delete_post(request, post_id):
    """删除文章"""
    post = get_object_or_404(BlogPost, id=post_id)

    # 权限检查：只能删自己的
    if post.owner != request.user:
        raise Http404("你没有权限删除此文章。")

    # 执行删除
    post.delete()
    return redirect('blogs:index')