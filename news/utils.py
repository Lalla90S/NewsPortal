from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post, Category



def send_new_post_notifications(post_id):
    """
    Отправляет уведомления подписчикам при добавлении новой статьи
    """
    try:
        post = Post.objects.get(id=post_id)

        # Получаем категории статьи
        categories = post.categories.all()

        # Для каждой категории получаем подписчиков
        for category in categories:
            subscribers = category.subscribers.all()

            for subscriber in subscribers:
                # Формируем HTML содержимое письма
                html_content = render_to_string(
                    'news/email/new_post_notification.html',
                    {
                        'post': post,
                        'username': subscriber.username,
                        'preview': post.text[:50] + '...' if len(post.text) > 50 else post.text
                    }
                )

                # Создаем письмо
                msg = EmailMultiAlternatives(
                    subject=post.title,  # Тема письма - заголовок статьи
                    body='',  # Текстовое содержимое (пустое, т.к. используем HTML)
                    from_email='newsportal@example.com',
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

    except Post.DoesNotExist:
        print("Статья не найдена")
    except Exception as e:
        print(f"Ошибка при отправке уведомлений: {e}")


def send_welcome_email(user_id):
    """
    Отправляет приветственное письмо новому пользователю
    """
    from django.contrib.auth.models import User

    try:
        user = User.objects.get(id=user_id)

        # Формируем URL для активации (пока используем главную страницу)
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
            subject=f'Добро пожаловать в News Portal, {user.username}!',  # Тема письма
            body='',  # Текстовое содержимое (пустое, т.к. используем HTML)
            from_email='newsportal@example.com',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print(f"Приветственное письмо отправлено пользователю {user.username}")

    except User.DoesNotExist:
        print("Пользователь не найден")
    except Exception as e:
        print(f"Ошибка при отправке приветственного письма: {e}")

