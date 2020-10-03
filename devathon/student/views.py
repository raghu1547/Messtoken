from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.views.generic import ListView
from student.models import Student
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import random
import smtplib
# Create your views here.
from vendor.models import Token, ExtraItems

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
        reg_id__user__username=request.user.username)
    print(tok_list)
    flag = False
    return render(request, 'student/dashboard.html', {'token_list': tok_list, 'flag': flag})


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


def generate_otp():
    return random.randint(100000, 999999)


def sendEmail(to, otp):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('singh_821916@student.nitw.ac.in', 'a1b2c3d4e5@avi')
        server.sendmail('singh_821916@student.nitw.ac.in', to,
                        f'Thanks for odering with us. Your OTP is {otp}.')
        server.close()
        return True
    except Exception as e:
        return False


@login_required
def placeOrder(request):
    extraItems = ExtraItems.objects.all()
    content = {
        "extraItems": extraItems,
    }
    if (request.method == "POST"):
        user = request.user
        otp = generate_otp()

        studentObj = Student.objects.filter(user=user)[0]
        userEmail = studentObj.email

        if sendEmail(userEmail, otp):
            studentObj.pass_code = otp
            studentObj.save()
            print("successful")
            content['statusSuccess'] = True
        else:
            content['statusFail'] = True
    return render(request, 'student/order.html', content)
