from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category
from django.contrib.auth.models import User


@shared_task
def send_new_post_notification(post_id):
    """
    Отправляет уведомления подписчикам при добавлении новой статьи
    """
    try:
        post = Post.objects.get(id=post_id)
        categories = post.categories.all()

        for category in categories:
            subscribers = category.subscribers.all()

            for subscriber in subscribers:
                if subscriber.email:
                    html_content = render_to_string(
                        'news/email/new_post_notification.html',
                        {
                            'post': post,
                            'username': subscriber.username,
                            'preview': post.text[:50] + '...' if len(post.text) > 50 else post.text
                        }
                    )

                    msg = EmailMultiAlternatives(
                        subject=post.title,
                        body='',
                        from_email='newsportal@example.com',
                        to=[subscriber.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

        return f"Уведомления отправлены для статьи: {post.title}"

    except Post.DoesNotExist:
        return "Статья не найдена"
    except Exception as e:
        return f"Ошибка при отправке уведомлений: {e}"


@shared_task
def send_weekly_digest():
    """
    Еженедельная рассылка новых статей подписчикам
    """
    try:
        week_ago = timezone.now() - timedelta(days=7)
        categories = Category.objects.all()
        emails_sent = 0

        for category in categories:
            new_posts = Post.objects.filter(
                categories=category,
                created_at__gte=week_ago
            ).order_by('-created_at')

            if new_posts.exists():
                subscribers = category.subscribers.all()

                for subscriber in subscribers:
                    if subscriber.email:
                        html_content = render_to_string(
                            'news/email/weekly_digest.html',
                            {
                                'username': subscriber.username,
                                'category': category,
                                'posts': new_posts,
                                'week_start': week_ago.strftime('%d.%m.%Y'),
                                'week_end': timezone.now().strftime('%d.%m.%Y'),
                            }
                        )

                        subject = f'Еженедельная подборка новых статей в категории "{category.name}"'

                        msg = EmailMultiAlternatives(
                            subject=subject,
                            body='',
                            from_email='newsportal@example.com',
                            to=[subscriber.email],
                        )
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        emails_sent += 1

        return f"Еженедельная рассылка отправлена. Всего писем: {emails_sent}"

    except Exception as e:
        return f"Ошибка при отправке еженедельной рассылки: {e}"


@shared_task
def send_welcome_email(user_id):
    """
    Отправляет приветственное письмо новому пользователю
    """
    try:
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id)

        # Формируем URL для активации
        activation_url = "http://127.0.0.1:8000/news/activation-success/"

        # Формируем HTML содержимое письма
        html_content = render_to_string(
            'news/email/welcome_email.html',
            {
                'username': user.username,
                'activation_url': activation_url,
            }
        )

        # Создаем письмо
        msg = EmailMultiAlternatives(
            subject=f'Добро пожаловать в News Portal, {user.username}!',
            body='',
            from_email='newsportal@example.com',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return f"Приветственное письмо отправлено пользователю {user.username}"

    except User.DoesNotExist:
        return "Пользователь не найден"
    except Exception as e:
        return f"Ошибка при отправке приветственного письма: {e}"