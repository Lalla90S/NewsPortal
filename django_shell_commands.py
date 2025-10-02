# Команды для выполнения в Django shell
# Запуск: python manage.py shell


# 1. Импорт необходимых моделей
from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

# 2. Создание двух пользователей
user1 = User.objects.create_user('user1', password='test123')
user2 = User.objects.create_user('user2', password='test123')

# 3. Создание двух объектов модели Author, связанные с пользователями
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# 4. Добавление 4 категорий в модель Category
category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Политика')
category3 = Category.objects.create(name='Образование')
category4 = Category.objects.create(name='Технологии')

# 5. Добавление 2 статей и 1 новости
post1 = Post.objects.create(
    author=author1,
    post_type=Post.ARTICLE,
    title='Первая статья о спорте',
    text='Это текст первой статьи о спорте. ' * 50  # Создаем длинный текст
)

post2 = Post.objects.create(
    author=author2,
    post_type=Post.ARTICLE,
    title='Вторая статья о политике',
    text='Это текст второй статьи о политике. ' * 50
)

post3 = Post.objects.create(
    author=author1,
    post_type=Post.NEWS,
    title='Новость о технологиях',
    text='Это текст новости о технологиях. ' * 50
)

# 6. Присвоение категорий (в одной статье/новости должно быть не меньше 2 категорий)
PostCategory.objects.create(post=post1, category=category1)
PostCategory.objects.create(post=post1, category=category4)  # У статьи 2 категории

PostCategory.objects.create(post=post2, category=category2)

PostCategory.objects.create(post=post3, category=category3)
PostCategory.objects.create(post=post3, category=category4)  # У новости 2 категории

# 7. Создание 4 комментариев к разным объектам модели Post
comment1 = Comment.objects.create(post=post1, user=user1, text='Отличная статья!')
comment2 = Comment.objects.create(post=post1, user=user2, text='Интересно, но можно лучше')
comment3 = Comment.objects.create(post=post2, user=user1, text='Согласен с автором')
comment4 = Comment.objects.create(post=post3, user=user2, text='Жду продолжения')

# 8. Применение like() и dislike() к статьям/новостям и комментариям
post1.like()  # +1 к рейтингу
post1.like()  # +1 к рейтингу
post1.dislike()  # -1 к рейтингу

post2.like()  # +1 к рейтингу
post2.like()  # +1 к рейтингу
post2.like()  # +1 к рейтингу

post3.dislike()  # -1 к рейтингу

comment1.like()  # +1 к рейтингу
comment1.like()  # +1 к рейтингу

comment2.dislike()  # -1 к рейтингу

comment3.like()  # +1 к рейтингу

comment4.dislike()  # -1 к рейтингу
comment4.dislike()  # -1 к рейтингу

# 9. Обновление рейтингов пользователей
author1.update_rating()
author2.update_rating()

# 10. Вывод username и рейтинг лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
print(f"Лучший пользователь: {best_author.user.username}, рейтинг: {best_author.rating}")

# 11. Вывод информации о лучшей статье
best_post = Post.objects.order_by('-rating').first()
print(f"Лучшая статья:")
print(f"Дата: {best_post.created_at}")
print(f"Автор: {best_post.author.user.username}")
print(f"Рейтинг: {best_post.rating}")
print(f"Заголовок: {best_post.title}")
print(f"Превью: {best_post.preview()}")

# 12. Вывод всех комментариев к лучшей статье
print(f"\nКомментарии к лучшей статье:")
comments = Comment.objects.filter(post=best_post)
for comment in comments:
    print(f"Дата: {comment.created_at}, Пользователь: {comment.user.username}, Рейтинг: {comment.rating}, Текст: {comment.text}")
