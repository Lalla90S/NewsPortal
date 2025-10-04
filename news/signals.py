from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .tasks import send_welcome_email

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    """Автоматически добавляет нового пользователя в группу common"""
    if created:  # Только для новых пользователей
        try:
            common_group = Group.objects.get(name='common')
            instance.groups.add(common_group)
            print(f"Пользователь {instance.username} добавлен в группу common")

            # Отправляем приветственное письмо новому пользователю ЧЕРЕЗ CELERY
            send_welcome_email.delay(instance.id)
            print(f"Задача отправки приветственного письма создана для {instance.username}")

        except Group.DoesNotExist:
            print("Группа 'common' не найдена")