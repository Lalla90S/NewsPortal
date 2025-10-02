from django import forms
from .models import Post, Author
from django.core.exceptions import ValidationError
from django.utils import timezone


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'categories': 'Категории',
        }

    def __init__(self, *args, **kwargs):
        # Извлекаем пользователя из kwargs перед передачей в родительский класс
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Проверяет, что пользователь не публикует более 3 новостей в сутки
        """
        cleaned_data = super().clean()

        # Используем пользователя переданного через __init__
        user = self.user

        if user and user.is_authenticated:
            # Проверяем количество новостей за последние 24 часа
            today = timezone.now()
            yesterday = today - timezone.timedelta(hours=24)

            # Находим автора для этого пользователя
            try:
                author = Author.objects.get(user=user)

                daily_posts = Post.objects.filter(
                    author=author,
                    created_at__gte=yesterday,  # новости за последние 24 часа
                    post_type=Post.NEWS  # только новости, не статьи
                ).count()

                if daily_posts >= 3:
                    raise ValidationError(
                        "❌ Вы не можете публиковать более 3 новостей в сутки. "
                        f"Вы уже опубликовали {daily_posts} новостей за последние 24 часа. "
                        "Попробуйте завтра или создайте статью вместо новости."
                    )

            except Author.DoesNotExist:
                # Если у пользователя нет автора, значит он еще не создавал постов
                # Можно создать автора или просто пропустить проверку
                pass

        return cleaned_data