from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Category

@shared_task
def send_weekly_newsletter():
    categories = Category.objects.all()
    for category in categories:
        subscribers = category.subscribers.all()
        subject = f'Weekly newsletter for category: {category.name}'
        message = f'Here are some articles that may interest you:\n\n'
        for article in category.articles.all().order_by('-created_at')[:5]:
            message += f'- {article.title}\n'
        from_email = 'noreply@yourdomain.com'
        recipient_list = [subscriber.email for subscriber in subscribers]
        send_mail(subject, message, from_email, recipient_list)

@shared_task
def schedule_weekly_newsletter():
    schedule_time = datetime.now() + timedelta(days=(6 - datetime.now().weekday()), hours=9)
    send_weekly_newsletter.apply_async(eta=schedule_time, repeat_every=604800)