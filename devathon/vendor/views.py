from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login
from .models import Token, ExtraItems, Transaction
from django.contrib.auth.admin import User
from student.models import Student
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import smtplib


def check(user):
    return not Student.objects.filter(user=user).exists()


@login_required
@user_passes_test(check)
def token_list(request):
    tok_list = Token.objects.filter(trans_id__status='A')
    # print(tok_list)
    flag = True
    return render(request, 'vendor/dashboard.html', {'token_list': tok_list, 'flag': flag})


# @login_required
# @user_passes_test(check)
# def order(request):
#     print(request.user)
#     if request.method == "POST":
#         print(request.POST)
#         reg_id = request.POST['reg_id']
#         Passcode = request.POST['Passcode']
#         try:
#             student = Student.objects.get(user__username=reg_id)
#             print(student)
#             if student.pass_code == Passcode:
#                 for item in request.POST:
#                     if item != 'reg_id' and item != 'Passcode' and item != 'csrfmiddlewaretoken':
#                         try:
#                             found = get_object_or_404(
#                                 ExtraItems, item_name=item)
#                             quantity = int(request.POST[item])
#                             if quantity > 0:
#                                 token = Token.objects.create(
#                                     reg_id=student, item_name=found, quantity=quantity)
#                                 token.save()
#                         except:
#                             pass
#                 return redirect('vendor:order')
#             else:
#                 return redirect('vendor:order')
#         except:
#             return redirect('vendor:order')
#     extraItems = ExtraItems.objects.all()
#     content = {
#         "extraItems": extraItems,
#     }
#     return render(request, 'vendor/order.html', content)


@login_required
@user_passes_test(check)
def pending(request):
    transaction = Transaction.objects.filter(status='P')
    # print(transaction)
    return render(request, 'vendor/pending.html', {'transaction': transaction})


def sendEmail(to, transid):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('singh_821916@student.nitw.ac.in', 'a1b2c3d4e5@avi')
        server.sendmail('singh_821916@student.nitw.ac.in', to,
                        f'This mail is to inform that your tokens for transaction {transid} have been issued. If it is not done by you Please write a complaint back.')
        server.close()
        return True
    except Exception as e:
        return False


@login_required
@user_passes_test(check)
def details(request, transid):
    if request.method == "POST":
        otp = request.POST["otp"]
        transaction = get_object_or_404(Transaction, trans_id=transid)
        # print("hai")
        if transaction.otp == otp:
            transaction.status = 'A'
            transaction.save()
            messages.success(request, "Tokens issued successfully")
            sendEmail(transaction.reg_id.user.email, transaction.trans_id)
            return redirect('vendor:pending')
        messages.error(request, "Please enter correct otp")
        return redirect('vendor:details', transid)
    transaction = get_object_or_404(Transaction, trans_id=transid)
    tok_list = Token.objects.filter(trans_id=transaction)
    # print(tok_list)
    # print(transaction)
    return render(request, 'vendor/details.html', {'transaction': transaction, 'token_list': tok_list})
