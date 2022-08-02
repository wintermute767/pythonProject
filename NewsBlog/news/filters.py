from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post


# создаём фильтр
class PostsFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = Post
        #fields = ('time_post', 'author_post', 'heading_post')
        fields = {
            'heading_post': ['icontains'],
            # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то, что запросил пользователь
            'time_post': ['gt'],  # количество товаров должно быть больше или равно тому, что указал пользователь
            #'author_post': ['icontains'],  # цена должна быть меньше или равна тому, что указал пользователь
        }
        # поля, которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)