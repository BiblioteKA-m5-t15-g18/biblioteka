import schedule
import time
from datetime import timedelta, datetime
from users.models import User
from loan.models import Loan
from django.utils import timezone

def job():
    print("schedule")
    # date_format = "%d-%m-%Y"
    # today = timezone.now()
    # current_date = datetime.strftime(today, date_format)
    # prazo = datetime.strftime(today - timedelta(days=1), date_format)
    # prazo = datetime.strftime(today + timedelta(days=7), date_format)
    # check = Loan.objects.all()
    # late_loans = []
    # for loan in check:
    #     prazo_loan = datetime.strftime(loan.prazo, date_format)
    #     if prazo_loan == prazo:
    #         late_loans.append(loan)
    # print(late_loans)
    # for late_loan in late_loans:
    #     instance_user = User.objects.filter(id=late_loan.user.id)
    #     instance_user["block"] = True
        # instance_user["timeBlock"] = today + timedelta(days=7)
        # instance_user["timeBlock"] = current_date + timedelta(days=7)

# schedule.every().day.at("05:15").do(job)
# schedule.every(3).seconds.do(job)

# while 1:
#     schedule.run_pending()
#     time.sleep(10)