# scheduler.py
import schedule
import time

class Scheduler:
    @staticmethod
    def schedule_job(job, time):
        schedule.every().day.at(time).do(job)

    @staticmethod
    def run():
        while True:
            schedule.run_pending()
            time.sleep(60)
