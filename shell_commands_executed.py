# Выполненные команды для Django shell
# Проект: News Portal

# 1. Импорт моделей
from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

# 2. Создание пользователей
user1 = User.objects.create_user('user1', password='test123')
user2 = User.objects.create_user('user2', password='test123')

# 3. Создание авторов
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# 4. Создание категорий
category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Политика')
category3 = Category.objects.create(name='Образование')
category4 = Category.objects.create(name='Технологии')

# 5. Создание постов
post1 = Post.objects.create(
    author=author1,
    post_type=Post.ARTICLE,
    title='Первая статья о спорте',
    text='Это текст первой статьи о спорте. ' * 50
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

# 6. Присвоение категорий
PostCategory.objects.create(post=post1, category=category1)
PostCategory.objects.create(post=post1, category=category4)
PostCategory.objects.create(post=post2, category=category2)
PostCategory.objects.create(post=post3, category=category3)
PostCategory.objects.create(post=post3, category=category4)

# 7. Создание комментариев
comment1 = Comment.objects.create(post=post1, user=user1, text='Отличная статья!')
comment2 = Comment.objects.create(post=post1, user=user2, text='Интересно, но можно лучше')
comment3 = Comment.objects.create(post=post2, user=user1, text='Согласен с автором')
comment4 = Comment.objects.create(post=post3, user=user2, text='Жду продолжения')

# 8. Лайки и дизлайки
post1.like()
post1.like()
post1.dislike()

post2.like()
post2.like()
post2.like()

post3.dislike()

comment1.like()
comment1.like()

comment2.dislike()

comment3.like()

comment4.dislike()
comment4.dislike()

# 9. Обновление рейтингов авторов
author1.update_rating()
author2.update_rating()

# 10. Лучший пользователь
best_author = Author.objects.order_by('-rating').first()
print(f"Лучший пользователь: {best_author.user.username}, рейтинг: {best_author.rating}")

# 11. Лучшая статья
best_post = Post.objects.order_by('-rating').first()
print(f"Лучшая статья:")
print(f"Дата: {best_post.created_at}")
print(f"Автор: {best_post.author.user.username}")
print(f"Рейтинг: {best_post.rating}")
print(f"Заголовок: {best_post.title}")
print(f"Превью: {best_post.preview()}")

# 12. Комментарии к лучшей статье
print(f"\nКомментарии к лучшей статье:")
comments = Comment.objects.filter(post=best_post)
for comment in comments:
    print(f"Дата: {comment.created_at}, Пользователь: {comment.user.username}, Рейтинг: {comment.rating}, Текст: {comment.text}")