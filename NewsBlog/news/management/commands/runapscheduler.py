import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from news.models import Post, Category, User
logger = logging.getLogger(__name__)

from NewsBlog.settings import LOCAL_HOST_HTTP
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def my_job():
    import datetime
    date = datetime.datetime.today()
    week = date.strftime("%V")
    # Your job processing logic here...
    print("__________________________")
    body_email=[]
    #получаем посты за неделю
    posts_last_week=Post.objects.filter(time_post__week=week)
    for user in User.objects.all():
        #Перебирам пользователей и находим тех кто пописан на категории и достаем id этих категорий
        category_id_sub_user=[n['id'] for n in (user.category_set.all().values('id'))]
        body_email=[]
        if category_id_sub_user:
            #Если пользователь все таки подписан на что либо то ищем посты из списка за неделю и убираем повторы
            post_to_send=set(posts_last_week.filter(category__in=category_id_sub_user))
            for post in post_to_send:

                email = {
                    "date": post.time_post,
                    "title": post.heading_post,
                    "post_url": LOCAL_HOST_HTTP + post.get_absolute_url(),
                    "message": post.preview(),
                }
                body_email.append(email)
                # формируем сам html
                html_content = render_to_string(
                    'mail/email_about_all_post_of_week.html',
                    {
                        'body_email': body_email,
                    }
                )

        msg = EmailMultiAlternatives(
            subject=f'Новые статьи за неделю',
            body='Body goes here',
            from_email='y4ndexp0chta766@yandex.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week ="*/6"),  # (second="*/10"), #Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")