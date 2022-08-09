from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post
from django.db import models


# создаём фильтр
class PostsFilter(FilterSet):

    class Meta:
        model = Post

        fields = {
            'time_post': ['gt'],
            # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то, что запросил пользователь
            'heading_post': ['icontains'],  # количество товаров должно быть больше или равно тому, что указал пользователь
            'author': ['exact'],  # цена должна быть меньше или равна тому, что указал пользователь
        }
