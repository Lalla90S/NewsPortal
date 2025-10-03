import os
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')
django.setup()

# Теперь запускаем планировщик
from news.scheduler import start_scheduler

if __name__ == "__main__":
    start_scheduler()
    print("Планировщик запущен. Нажми Ctrl+C для остановки.")

    try:
        # Бесконечный цикл чтобы планировщик работал
        import time

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Планировщик остановлен.")