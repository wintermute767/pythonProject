from django.urls import path
from .views import PostsList, PostDetail, SearchList

urlpatterns = [

    path('', PostsList.as_view(), name='home'),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', SearchList.as_view(), name='search'),
]
