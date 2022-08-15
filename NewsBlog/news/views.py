from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
from .filters import PostsFilter
from .forms import PostForm
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime

class PostsList(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 3

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def post(self, *args, **kwargs):


        appointment = {
            "date": PostDetail.get_object(self).time_post,
            "client_name":self.request.user.username,
            "message": PostDetail.get_object(self).text_post,
        }

        html_content = render_to_string(
            'email.html',
            {
                'appointment': appointment,
            }
        )
        msg = EmailMultiAlternatives(
            PostDetail.get_object(self).heading_post,
            PostDetail.get_object(self).preview(),
            'y4ndexp0chta766@yandex.ru',
            ['andrew_catboy@mail.ru'],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()
        return redirect('home')

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostsFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/search'
    permission_required = ('news.delete_post',)
