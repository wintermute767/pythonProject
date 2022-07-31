from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
# Create your models here.


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

class Category(models.Model):
    name_category = models.CharField(max_length=64, default="Unknown", unique = True)

class Post(models.Model):
    article = 'AR'
    news = 'NE'

    TYPE_POST = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    types_post = models.CharField(max_length=2, choices=TYPE_POST, default=news)
    author_post = models.ForeignKey(Author, on_delete = models.CASCADE)
    time_post = models.DateTimeField(auto_now_add=True)
    category_post = models.ManyToManyField(Category, through = 'PostCategory')
    heading_post = models.CharField(max_length=128, default="Something")
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -=1
        self.save()

    def preview(self):
        return self.text_post[0:124]+"..."

class PostCategory(models.Model):
    post_category = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_post = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -=1
        self.save()

    def __str__(self):
        try:
            return self.post_comment.author_post.post_author.username
        except:
            return self.post_comment.username