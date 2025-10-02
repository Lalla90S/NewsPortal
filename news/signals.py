from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .utils import send_welcome_email
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Category

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    """Автоматически добавляет нового пользователя в группу common"""
    if created:  # Только для новых пользователей
        try:
            common_group = Group.objects.get(name='common')  # Ищем группу common
            instance.groups.add(common_group)  # Добавляем в common
            print(f"Пользователь {instance.username} добавлен в группу common")  # Для отладки

            # Отправляем приветственное письмо новому пользователю
            send_welcome_email(instance.id)
            print(f"Приветственное письмо отправлено для {instance.username}")

        except Group.DoesNotExist:
            print("Группа 'common' не найдена")  # Для отладки


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    """
    Отправляет email-уведомления подписчикам при создании новой новости
    """
    if created and instance.post_type == Post.NEWS:
        print(f"Создана новая новость: {instance.title}")

        # Получаем категории новости
        categories = instance.categories.all()

        for category in categories:
            # Получаем всех подписчиков категории
            subscribers = category.subscribers.all()
            print(f"Категория '{category.name}' имеет {subscribers.count()} подписчиков")

            for subscriber in subscribers:
                if subscriber.email:  # Проверяем, есть ли email у пользователя
                    try:
                        # Формируем тему и сообщение
                        subject = f'Новая новость в категории "{category.name}"'

                        message = f'''
                        Здравствуйте, {subscriber.username}!

                        В категории "{category.name}" опубликована новая новость:

                        Заголовок: {instance.title}
                        Анонс: {instance.text[:50]}...

                        Читать полностью: http://127.0.0.1:8000/news/{instance.id}/

                        С уважением,
                        Команда News Portal
                        '''

                        # Отправляем email
                        send_mail(
                            subject=subject,
                            message=message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[subscriber.email],
                            fail_silently=False,  # Показывать ошибки если есть
                        )

                        print(f"Отправлено уведомление для {subscriber.email}")

                    except Exception as e:
                        print(f"Ошибка отправки email для {subscriber.email}: {e}")