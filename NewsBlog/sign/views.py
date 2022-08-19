from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import User, Author

class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    if not Author.objects.filter(post_author=User.objects.get(username=user)).exists():
        user_in_author = User.objects.get(username=user)
        Author.objects.create(post_author=user_in_author)
    return redirect('home')