from django.urls import path
from .views import UserView, LogoutView, upgrade_me

urlpatterns = [
    path('user/', UserView.as_view(template_name = 'sign/user.html'), name='user'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('upgrade/', upgrade_me, name = 'upgrade')
]