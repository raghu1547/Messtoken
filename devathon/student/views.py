from devathon.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponse
from django.views.generic import ListView
from student.models import Student
from django.shortcuts import render, redirect
from vendor.models import ExtraItems, Token, Transaction
from django.shortcuts import get_object_or_404
# Create your views here.
from vendor.models import Token
from django.contrib import messages
import random
import smtplib

from django.contrib.auth import get_user_model

User = get_user_model()


"""
def check(user):
    try:
        print('in try')
        S = get_object_or_404(Student,user=user)
        if S:
            return True
    except:
        print('in expect')
        return False

"""
"""
def check(user):
    if Student.objects.get(user=user):
        return True
    else:
        return False

"""


def check(user):
    return Student.objects.filter(user=user).exists()


@login_required
@user_passes_test(check)
def userlist(request):
    tok_list = Token.objects.filter(
        trans_id__reg_id__user__username=request.user.username).filter(trans_id__status='A')
    # print(tok_list)
    due_total = 0
    for tok in tok_list:
        due_total += ((int(tok.item_name.item_cost))*(int(tok.quantity)))

    return render(request, 'student/dashboard.html', {'token_list': tok_list, 'due_total': due_total})


"""
class UserToken(ListView):
    model = Token
    template_name = 'student/dashboard.html'

    def get_queryset(self):
        try:
            self.token_user = Student.objects.prefetch_related('token').get(username__iexact=)
        except User.DoesNotExist:
            print("jkdb")
            raise Http404
        else:
            return self.post_user.token.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tokenuser'] = self.token_user
        return context
"""


def createTranId():
    transId = random.randint(100000000, 999999999)
    count = 20
    while count > 0:
        if Transaction.objects.filter(trans_id=transId).exists():
            count = count - 1
            transId = random.randint(100000000, 999999999)
        else:
            break
    if count == 0:
        return HttpResponse('Could not create transaction ID Try again after a while', status=405)
    return transId


def generate_otp():
    return random.randint(100000, 999999)


def sendEmail(to, transid, otp):
    print(to)
    try:
        server = smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
        server.ehlo()
        server.starttls()
        print(server.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD))
        server.sendmail(EMAIL_HOST_USER, to,
                        f'Thanks for odering with us. Your OTP for transaction {transid} is {otp}.')
        server.close()
        return True
    except Exception as e:
        return False


@login_required
@user_passes_test(check)
def order(request):
    if Transaction.objects.filter(reg_id__user=request.user, status='P').count() >= 10:
        flag = True
        return render(request, 'student/order.html', {'flag': flag})
    if request.method == "POST":
        try:
            student = Student.objects.get(user=request.user)
            quants = []
            # print(student)
            for item in request.POST:
                if item != 'csrfmiddlewaretoken':
                    try:
                        found = get_object_or_404(
                            ExtraItems, item_name=item)
                        quantity = int(request.POST[item])
                        if quantity > 0:
                            quants.append((quantity, found))
                            # print(quantity)
                    except:
                        pass
            if len(quants):
                transid = createTranId()
                otp = generate_otp()
                # print(transid, otp)
                transaction = Transaction(
                    trans_id=transid, reg_id=student, otp=otp)
                transaction.save()
                for item in quants:
                    # print(item)
                    token = Token.objects.create(
                        trans_id=transaction, item_name=item[1], quantity=item[0])
                    token.save()
                # print(request.user.email)
                if sendEmail(request.user.email, transid, otp):
                    # print("kriabsf")
                    messages.success(request, "Order Placed successfully")
                return redirect('student:placeorder')
            else:
                messages.error(request, "Don't fill fake forms")
                return redirect('student:placeorder')
        except:
            messages.error(request, "Something went wrong")
            return redirect('student:placeorder')
    extraItems = ExtraItems.objects.all()
    content = {
        "extraItems": extraItems,
    }
    return render(request, 'student/order.html', content)


@login_required
@user_passes_test(check)
def pending(request):
    transaction = Transaction.objects.filter(
        reg_id__user=request.user, status='P')
    # print(transaction)
    return render(request, 'student/pending.html', {'transaction': transaction})


@login_required
@user_passes_test(check)
def details(request, transid):
    transaction = get_object_or_404(Transaction, trans_id=transid)
    tok_list = Token.objects.filter(trans_id=transaction)
    # print(tok_list)
    # print(transaction)
    return render(request, 'student/details.html', {'transaction': transaction, 'token_list': tok_list})
