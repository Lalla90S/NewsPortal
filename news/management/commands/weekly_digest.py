from django.core.management import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from news.models import Category, Post


class Command(BaseCommand):
    help = 'Еженедельная рассылка новых статей подписчикам'

    def handle(self, *args, **options):
        # Определяем период за последнюю неделю
        week_ago = timezone.now() - timedelta(days=7)

        # Получаем все категории
        categories = Category.objects.all()

        for category in categories:
            # Получаем новые статьи в этой категории за последнюю неделю
            new_posts = Post.objects.filter(
                categories=category,
                created_at__gte=week_ago
            ).order_by('-created_at')

            if new_posts.exists():
                # Получаем подписчиков категории
                subscribers = category.subscribers.all()

                for subscriber in subscribers:
                    if subscriber.email:  # Проверяем, что у пользователя есть email
                        self.send_weekly_digest(subscriber, category, new_posts)

        self.stdout.write(
            self.style.SUCCESS('Еженедельная рассылка успешно отправлена')
        )

    def send_weekly_digest(self, subscriber, category, posts):
        """Отправляет еженедельную подборку статей"""

        # Формируем HTML содержимое письма
        html_content = render_to_string(
            'news/email/weekly_digest.html',
            {
                'username': subscriber.username,
                'category': category,
                'posts': posts,
                'week_start': (timezone.now() - timedelta(days=7)).strftime('%d.%m.%Y'),
                'week_end': timezone.now().strftime('%d.%m.%Y'),
            }
        )

        # Создаем письмо
        subject = f'Еженедельная подборка новых статей в категории "{category.name}"'

        msg = EmailMultiAlternatives(
            subject=subject,
            body='',  # Текстовое содержимое (пустое, т.к. используем HTML)
            from_email='newsportal@example.com',
            to=[subscriber.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        self.stdout.write(
            f'Отправлена рассылка для {subscriber.username} '
            f'по категории {category.name} ({len(posts)} статей)'
        )
