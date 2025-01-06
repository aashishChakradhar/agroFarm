from celery import shared_task

@shared_task
def my_periodic_task():
    print("Running my periodic script...")