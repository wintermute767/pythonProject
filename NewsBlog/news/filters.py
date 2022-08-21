from django_filters import FilterSet
from .models import Post
from django.db import models


# создаём фильтр
class PostsFilter(FilterSet):

    class Meta:
        model = Post

        fields = {
            'time_post': ['gt'],
            'heading_post': ['icontains'],
            'author': ['exact'],
        }
