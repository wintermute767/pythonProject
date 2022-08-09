from django.forms import ModelForm
from .models import Post
from django.db import models

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ["types_post", "author", "category", "heading_post", "text_post"]