from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events
from django.utils import timezone
import sys
from datetime import timedelta, datetime
from users.models import User
from loan.models import Loan
from follow.models import Follow
from copies.models import Copy
from book.models import Book
from django.core.mail import send_mail
from django.conf import settings


def job():
    date_format = "%d-%m-%Y"
    today = timezone.now()
    today_formated = datetime.strftime(today, date_format)
    check = Loan.objects.all()
    late_loans = []

    for loan in check:
        prazo_loan = datetime.strftime(loan.term, date_format)
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

    follows = Follow.objects.all()
    for follow in follows:
        copies = Copy.objects.filter(book_id=follow.book).all()
        user = User.objects.get(id=follow.user.id)
        book = Book.objects.get(id=follow.book.id)
        for copy in copies:
            if copy.available:
                send_mail(
                    subject="Biblioteka",
                    message=f'Olá, {user.name}! O livro {book.title} que você está seguindo, acabou de ficar disponível. Corra antes que alguém pegue!',
                    recipient_list=[user.email],
                    from_email=settings.EMAIL_HOST_USER,
                    fail_silently=False
                )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, "cron", hour=5, name='clean_accounts')  # noqa
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)
