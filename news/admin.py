from django.contrib import admin
from .models import Category, CategorySubscriber, Post, PostCategory, Comment, Author
from django.core.cache import cache






# Регистрируем модель Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        """
        Сбрасываем кэш при сохранении категории в админке
        """
        cache.delete('all_categories_list')
        cache.delete_pattern('*categories_list*')
        print("Кэш категорий сброшен из админки")
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Сбрасываем кэш при удалении категории из админки
        """
        cache.delete('all_categories_list')
        cache.delete_pattern('*categories_list*')
        print("Кэш категорий сброшен из админки при удалении")
        super().delete_model(request, obj)


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
