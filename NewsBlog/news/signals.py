from django.db.models.signals import post_save, m2m_changed # импортируем нужный сигнал
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from NewsBlog.settings import LOCAL_HOST_HTTP


@receiver(m2m_changed, sender=Post.category.through)
def notify_category_update(sender, instance, action, **kwargs):
    if action == "post_add":
        post = Post.objects.get(pk=instance.id)
        categoryes = [s.name_category for s in post.category.all()]
        user_subscribers=set()
        for category in categoryes:
            for user in Category.objects.get(name_category=category).subscribers.all():
                print(user.email)
                user_subscribers.add(user.email)

        #содержимое html
        email = {
            "date": post.time_post,
            "title":post.heading_post,
            "post_url":LOCAL_HOST_HTTP+post.get_absolute_url(),
            "message": post.preview(),
        }

        # формируем сам html
        html_content = render_to_string(
            'mail/email_about_post.html',
            {
                'email': email,
            }
        )

        msg = EmailMultiAlternatives(
            subject=post.heading_post,
            body=email["message"],
            from_email='y4ndexp0chta766@yandex.ru',
            to=user_subscribers,
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()


