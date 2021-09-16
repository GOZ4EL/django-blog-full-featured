"""
Unit Tests for the blog app.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Post


def create_multiple_posts(number_of_posts):
    """
    Create n number of posts, being n
    the 'number_of_posts' argument.
    """
    user = User.objects.create(username='authuser',
                                   password='t3stu$3erF0rP0sT')
    posts = []
    for i in range(number_of_posts):
        post = create_post(title=f'Test Post {i}', slug=f'p{i}',
                           author=user, body=f'Example number {i}')
        posts.append(post)
    posts.reverse()
    return posts


def create_post(title, slug, author, body, status='published'):
    """
    Create a Post with the given title, author, body
    and status.
    """
    return Post.objects.create(title=title, slug=slug, 
                               author=author, body=body, 
                               status=status)


class PostListViewTests(TestCase):
    """
    Contains all 'post_list' view unit tests.
    """
    def test_posts_with_draft_status(self):
        """
        Posts 'with' draft status aren't displayed on the post list.
        """
        user = User.objects.create(username='authuser',
                                   password='sahfdsau1324$9\'%')
        post = create_post(title='Test Post', slug='test', author=user,
                           body='This is a post with the draft status',
                           status='draft')
        response = self.client.get(reverse('blog:post_list'))
        self.assertQuerysetEqual(response.context['posts'], [],)

    def test_post_with_published_status(self):
        """
        Posts with 'published' status are displayed on the post list.
        """
        user = User.objects.create(username='authuser',
                                   password='t3stu$3erF0rP0sT')
        post = create_post(title='Test Post', slug='Test', author=user,
                           body='This is a post with the published status.')
        response = self.client.get(reverse('blog:post_list'))
        self.assertQuerysetEqual(response.context['posts'], [post])

    def test_draft_and_published_posts(self):
        """
        Even if both posts with 'published' and 'draft' status exists,
        only those whose status is 'published' are displayed.
        """
        user = User.objects.create(username='authuser',
                                   password='t3stu$3erF0rP0sT')
        draft_post = create_post(title='Test Post', slug='draft-post',
                                 author=user, status='draft',
                                 body='This is the draft one.')
        published_post = create_post(title='Test Post 2', slug='published-post',
                                     author=user, body='This is the published one.')
        response = self.client.get(reverse('blog:post_list'))
        self.assertQuerysetEqual(response.context['posts'], 
                                 [published_post])

    def test_three_posts(self):
        """
        The post list may display multiple posts.
        """
        posts = create_multiple_posts(3)
        response = self.client.get(reverse('blog:post_list'))
        self.assertQuerysetEqual(response.context['posts'], posts)

    def test_first_page(self):
        """
        The first page of the post list may 
        show the last three added posts.
        """
        posts = create_multiple_posts(7)
        response = self.client.get(reverse('blog:post_list'), 
                                   {'page': 1})
        self.assertQuerysetEqual(response.context['posts'], posts[:3]) 

    def test_last_page(self):
        """
        the last page of the post lists may 
        show the first post that has ever been made.
        """
        posts = create_multiple_posts(7)
        response = self.client.get(reverse('blog:post_list'),
                                   {'page': 3})
        self.assertQuerysetEqual(response.context['posts'], [posts[-1]])
