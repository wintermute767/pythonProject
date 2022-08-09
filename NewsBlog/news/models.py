from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum



class Author(models.Model):
    post_author = models.OneToOneField(User, on_delete = models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating_post'))
        pRat =0
        pRat+=postRat.get('postRating')

        commentRat = self.post_author.comment_set.all().aggregate(commentRating=Sum('rating_comment'))
        cRat=0
        cRat+=commentRat.get('commentRating')

        self.rating_author = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return self.post_author.username

class Category(models.Model):
    name_category = models.CharField(max_length=64, default="Unknown", unique = True)

    def __str__(self):
        return self.name_category

class Post(models.Model):
    article = 'AR'
    news = 'NE'

    TYPE_POST = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    types_post = models.CharField(max_length=2, choices=TYPE_POST, default=news)
    author = models.ForeignKey(Author, on_delete = models.CASCADE, default=1)
    time_post = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through = 'PostCategory', default=1)
    heading_post = models.CharField(max_length=128, default="Something")
    text_post = models.TextField(default="Something")
    rating_post = models.IntegerField(default=0)



    def get_absolute_url(self):
        return f'/{self.id}'

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -=1
        self.save()

    def preview(self):
        return self.text_post[0:124]+"..."

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostCategory(models.Model):
    post_category = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_post = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text_comment = models.TextField()
    time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -=1
        self.save()
