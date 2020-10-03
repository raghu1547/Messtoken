from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login
from .models import Token, ExtraItems
from django.contrib.auth.admin import User
from student.models import Student
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required,user_passes_test



def check(user):
    return not Student.objects.filter(user=user).exists()

@login_required
@user_passes_test(check)
def token_list(request):
    tok_list = Token.objects.all()
    print(tok_list)
    flag = True
    return render(request,'vendor/dashboard.html',{'token_list':tok_list,'flag':flag})

@login_required
@user_passes_test(check)
def order(request):
    print(request.user)
    if request.method == "POST":
        print(request.POST)
        reg_id = request.POST['reg_id']
        Passcode = request.POST['Passcode']
        try:
            student = Student.objects.get(user__username=reg_id)
            print(student)
            if student.pass_code == Passcode:
                for item in request.POST:
                    if item != 'reg_id' and item != 'Passcode' and item != 'csrfmiddlewaretoken':
                        try:
                            found = get_object_or_404(
                                ExtraItems, item_name=item)
                            quantity = int(request.POST[item])
                            if quantity > 0:
                                token = Token.objects.create(
                                    reg_id=student, item_name=found, quantity=quantity)
                                token.save()
                        except:
                            pass
                return redirect('vendor:order')
            else:
                return redirect('vendor:order')
        except:
            return redirect('vendor:order')
    extraItems = ExtraItems.objects.all()
    content = {
        "extraItems": extraItems,
    }
    return render(request, 'vendor/order.html', content)
