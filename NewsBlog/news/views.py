from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Post
from .filters import PostsFilter
from .forms import PostForm

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


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostsFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostCreateView(CreateView):
    template_name = 'create.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = 'create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/search'

