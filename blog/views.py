"""
This module contains all the views logic of the post model.
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import(
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


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

