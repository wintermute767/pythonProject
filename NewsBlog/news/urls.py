from django.urls import path
from .views import PostsList, PostDetail, SearchList, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [

    path('', PostsList.as_view(), name='home'),
    path('<int:pk>', PostDetail.as_view(), name='detail'),
    path('search/', SearchList.as_view(), name='search'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
]
