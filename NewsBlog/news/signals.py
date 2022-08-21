from django.db.models.signals import post_save, m2m_changed # импортируем нужный сигнал
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from .views import PostCreateView


@receiver(m2m_changed, sender=Post.category.through)
def notify_category_update(sender, instance, action, **kwargs):
    if action == "post_add":
        post = Post.objects.get(pk=instance.id)
        categoryes = [s.name_category for s in post.category.all()]
        for category in categoryes:
            for user in Category.objects.get(name_category=category).subscribers.all():
                #содержимое html
                email = {
                    "date": post.time_post,
                    "client_name": user.username,
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
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()




"""@receiver(m2m_changed, sender=Post.category.through)
def notify_managers_appointment(sender, instance, action, **kwargs):
    if action == "post_add":
        post = Post.objects.get(pk=instance.id)
        print(post.category.all())
        categoryes = [s.name_category for s in post.category.all()]
        for cat in categoryes:
            print(Category.objects.get(name_category=cat).subscribers)

    #print(instance.category_set.all())
    
    user_now = request.user
    category_now = Category.objects.get(name_category=PostDetail.get_object(self).get_category())
    if not user_now.category_set.filter(name_category=category_now).exists():
        user_now.category_set.add(category_now)
    содержимое html
    email = {
        "date": PostDetail.get_object(sender).time_post,
        "client_name":sender.request.user.username,
        "message": PostDetail.get_object(sender).preview(),
    }
    #формируем сам html
    html_content = render_to_string(
        'mail/email_about_post.html',
        {
            'email': email,
        }
    )
    #содержимое письма
    msg = EmailMultiAlternatives(
        subject=PostDetail.get_object(sender).heading_post,
        body=email["message"],
        from_email='y4ndexp0chta766@yandex.ru',
        to=[sender.request.user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()"""

"""@receiver(m2m_changed, sender=Post.category.through)
def notify_users_news(sender, instance, action, **kwargs):
    print(instance)
    if action == "post_add":
        post = Post.objects.get(pk=instance.id)
        categoryes = [s.name_category for s in post.category.all()]
        print(categoryes)

        if categoryes:
            for category in categorys:
                print(category)
                #list_email_subscriptions = [d.subscribersUser.email for d in Subscriber.objects.filter(postCategory=Category.objects.get(name=cat))]


            if list_email_subscriptions:
                for email in list_email_subscriptions:
                    html_content = render_to_string(
                        'mail_send.html',
                        {
                            'new': post,
                            'email': email,
                        }
                    )

                    msg = EmailMultiAlternatives(
                        subject=f'Здравствуй. Новая статья в твоём любимом разделе!',
                        body=f'Это автоматическая рассылка.',
                        from_email=f'dnetdima@gmail.com',
                        to=[email,],
                    )
                    msg.attach_alternative(html_content, "text/html")

                    try:
                        print('send')
                        #msg.send()
                    except:
                        raise SMTPDataError(554, 'Сообщение отклонено по подозрению в спаме!')"""