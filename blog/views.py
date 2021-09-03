"""
This module contains all the views logic of the post model.
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import(
    Paginator,
    EmptyPage,
    PageNotAnInteger
)

from .models import Post


def post_list(request):
    """
    Render all published posts.
    """
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    """
    Render the details of a specific post.
    """
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

