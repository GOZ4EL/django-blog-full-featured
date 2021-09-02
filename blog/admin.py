"""
This module defines which models can be used on the administration site.
"""
from django.contrib import admin
from .models import Post

admin.site.register(Post)

