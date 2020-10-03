from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from student.models import Student

from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.user.is_authenticated:
        try:
            Student.objects.get(user=request.user)
            return redirect('student:dashboard')
        except:
            return redirect('vendor:dashboard')
     
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        #print(user.password)
        if user is not None :
            if user.is_active:
                login(request, user)
                print("hvedu")
                try:
                    Student.objects.get(user=user)
                    return redirect('student:dashboard')
                except:
                    return redirect('vendor:dashboard')
                
            else:
                return HttpResponse('h1You are not an Active user')
        else:
            return HttpResponse('Please input the correct details')
    return render(request,'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect("accounts:login")


