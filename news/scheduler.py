from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.management import call_command
from django_apscheduler import util
from django.conf import settings


def start_weekly_digest():
    """Запускает еженедельную рассылку"""
    print("Запуск еженедельной рассылки...")
    call_command('weekly_digest')


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Удаляет старые записи о выполнении задач из БД.
    max_age по умолчанию 7 дней.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def start_scheduler():
    """Запускает планировщик задач только после полной инициализации Django"""

    # Проверяем, не запущен ли уже планировщик
    if hasattr(settings, 'SCHEDULER_STARTED') and settings.SCHEDULER_STARTED:
        return

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Еженедельная рассылка - каждый понедельник в 9:00
    scheduler.add_job(
        start_weekly_digest,
        trigger=CronTrigger(day_of_week="mon", hour=9, minute=0),
        id="weekly_digest",
        max_instances=1,
        replace_existing=True,
    )

    # Очистка старых задач - каждый день в 00:00
    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(hour=0, minute=0),
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )

    try:
        scheduler.start()
        # Помечаем, что планировщик запущен
        settings.SCHEDULER_STARTED = True
        print("✅ Планировщик задач запущен!")
        print("📅 Еженедельная рассылка будет отправляться каждый понедельник в 9:00")
    except Exception as e:
        print(f"❌ Ошибка запуска планировщика: {e}")