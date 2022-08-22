from datetime import date

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Category, Author
from .filters import PostsFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.db.models.signals import post_save

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

    def post(self, request, *args, **kwargs):

        #Проверяем есть ли подписан ли пользователь на текущую категорию
        #Если нет, то добавлем его на подписку и выслыаем письмо на почту
        user_now = self.request.user
        category_now= Category.objects.get(name_category=PostDetail.get_object(self).get_category())
        if not user_now.category_set.filter(name_category=category_now).exists():
            user_now.category_set.add(category_now)


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

    def form_valid(self, form):

        if Post.objects.filter(time_post__gte=date.today(), author=Author.objects.get(post_author=self.request.user)).count() < 3:
            print("Сохранение объекта Author.objects.get(post_author=self.request.user)")
            self.object = form.save(commit=False)
            self.object.author = Author.objects.get(post_author=self.request.user)
            return super().form_valid(form)
        else:
            return redirect('home')


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
