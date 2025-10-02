from django.contrib import admin
from .models import Category, CategorySubscriber, Post, PostCategory, Comment, Author

# Регистрируем модель Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # что показывать в списке
    search_fields = ('name',)  # по каким полям можно искать

# Регистрируем модель CategorySubscriber
class CategorySubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'subscribed_at')
    list_filter = ('category', 'subscribed_at')  # фильтры справа

# Регистрируем остальные модели
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_type', 'created_at', 'rating')
    list_filter = ('post_type', 'categories', 'created_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'rating')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')

# Регистрируем все модели в админке
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategorySubscriber, CategorySubscriberAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)