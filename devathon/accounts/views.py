from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from student.models import Student
from .forms import UserRegForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.admin import User


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
        # print(user.password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    Student.objects.get(user=user)
                    return redirect('student:dashboard')
                except:
                    return redirect('vendor:dashboard')
            else:
                messages.error(request, "Username not Active")
                return redirect('accounts:login')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect("accounts:login")


def regUser(form):
    user = User.objects.create_user(username=form['username'], first_name=form['first_name'],
                                    last_name=form['last_name'], email=form['email'], password=form['password1'])
    user.save()
    student = Student(user=user, pass_code="-1")
    student.save()


def user_register(request):
    if request.user.is_authenticated:
        try:
            Student.objects.get(user=request.user)
            return redirect('student:dashboard')
        except:
            return redirect('vendor:dashboard')
    if request.method == "POST":
        form = UserRegForm(request.POST)
        if form.is_valid():
            # print(form['username'])
            # print(form.cleaned_data)
            regUser(form.cleaned_data)
            messages.success(request, "Registration Successful")
            return redirect('accounts:login')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            return redirect("accounts:register")
    else:
        return render(request, 'accounts/register.html')
