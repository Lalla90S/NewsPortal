from django.core.cache import cache
from .models import Category


def categories(request):
    """
    Добавляет список всех категорий в контекст всех шаблонов
    """
    # Используем более уникальный ключ для кэша
    cache_key = 'all_categories_list'
    categories_list = cache.get(cache_key)

    if not categories_list:
        # Если в кэше нет, получаем из базы и сохраняем в кэш
        categories_list = Category.objects.all()
        cache.set(cache_key, categories_list, 60 * 60)  # Кэшируем на 1 час
        print("Категории загружены из базы и сохранены в кэш")
    else:
        print("Категории загружены из кэша")

    return {
        'categories': categories_list
    }