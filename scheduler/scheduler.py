from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events
from django.utils import timezone
import sys
from datetime import timedelta
from users.models import User
from loan.models import Loan
from follow.models import Follow
from copies.models import Copy
from book.models import Book
from django.core.mail import send_mail
from django.conf import settings


def job():
    today = timezone.now()
    tomorrow = today + timedelta(days=1)
    loans = Loan.objects.all()
    late_loans = []
    for loan in loans:
        if today > loan.term and loan.returned == False:
            late_loans.append(loan)
        if loan.term.date() == tomorrow.date():
            loan_copy = Copy.objects.get(loan=loan.id)
            loan_user = User.objects.get(id=loan.user.id)
            loan_book = Book.objects.get(id=loan_copy.book.id)
            send_mail(
                subject="Biblioteka - aviso de prazo de empréstimo",
                message=f'Olá, {loan_user.name}! O prazo de devolução do livro {loan_book.title} termina amanhã!',
                recipient_list=[loan_user.email],
                from_email=settings.EMAIL_HOST_USER,
                fail_silently=False
            )

    for late_loan in late_loans:
        late_loan_user = User.objects.get(id=late_loan.user.id)
        late_loan_copy = Copy.objects.get(loan=late_loan.id)
        late_loan_book = Book.objects.get(id=late_loan_copy.book.id)
        late_loan_user.block = True
        late_loan_user.timeBlock = today + timedelta(days=7)
        late_loan_user.save()
        send_mail(
            subject="Biblioteka - aviso de bloqueio",
            message=f'Olá, {late_loan_user.name}! Você acaba de ficar bloqueado para novos empréstimos por 7 dias! Faça a devolução do livro {late_loan_book.title} para o bloqueio não ser renovado!',
            recipient_list=[late_loan_user.email],
            from_email=settings.EMAIL_HOST_USER,
            fail_silently=False
        )

    users = User.objects.all()
    for user in users:
        if today > user.timeBlock and user.block:
            user.block = False
            user.timeBlock = None
            user.save()

    follows = Follow.objects.all()
    for follow in follows:
        follow_copies = Copy.objects.filter(book_id=follow.book).all()
        follow_user = User.objects.get(id=follow.user.id)
        follow_book = Book.objects.get(id=follow.book.id)
        for copy in follow_copies:
            if copy.available:
                send_mail(
                    subject="Biblioteka - aviso de disponibilidade",
                    message=f'Olá, {follow_user.name}! O livro {follow_book.title} que você está seguindo, acabou de ficar disponível. Corra antes que alguém pegue!',
                    recipient_list=[follow_user.email],
                    from_email=settings.EMAIL_HOST_USER,
                    fail_silently=False
                )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, "cron", hour=5, name='clean_accounts')
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)