from django.urls import path
from .views import UserView, upgrade_me
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('user/', UserView.as_view(template_name = 'sign/user.html'), name='user'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('upgrade/', upgrade_me, name = 'upgrade')
]