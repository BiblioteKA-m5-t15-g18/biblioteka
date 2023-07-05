from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from datetime import timedelta, datetime
from users.models import User
from loan.models import Loan


# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def job():
    print('schedule')
    date_format = "%d-%m-%Y"
    today = timezone.now()
    today_formated = datetime.strftime(today, date_format)
    check = Loan.objects.all()
    late_loans = []

    for loan in check:
        prazo_loan = datetime.strftime(loan.prazo, date_format)
        if prazo_loan < today_formated:
            late_loans.append(loan)

    for late_loan in late_loans:
        instance_user = User.objects.get(id=late_loan.user.id)
        instance_user.block = True
        instance_user.timeBlock = today + timedelta(days=7)
        instance_user.save()

    users = User.objects.all()
    for user in users:
        if user.block:
            user_time_block = datetime.strftime(user.timeBlock, date_format)
            if user_time_block < today_formated:
                user.block = False
                user.timeBlock = None
                user.save()


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every 24 hours
    scheduler.add_job(job, 'cron', hour="5", name='clean_accounts', jobstore='default')
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)
