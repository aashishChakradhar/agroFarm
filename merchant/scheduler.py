from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from merchant.tasks import fetch_and_store_data  # Import the task
import logging

logging.basicConfig(level=logging.INFO)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_and_store_data,
        trigger=IntervalTrigger(hours=2),
        id="fetch_and_store_data",
        replace_existing=True
    )
    scheduler.start()
    logging.info("Scheduler started for fetching API data.")