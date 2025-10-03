from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        """
        Метод автоматически вызывается при загрузке приложения
        Здесь мы импортируем сигналы, чтобы они зарегистрировались
        """
        import news.signals
        print("Сигналы приложения news загружены")  # Для отладки

