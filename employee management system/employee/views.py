from django.shortcuts import render, get_object_or_404
from employee.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate, login, logout
from django import forms
from employee.forms import UserForm
from django.urls import reverse
from django.http import Http404, HttpResponse

# Create your views here.

def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('employee_list'))

        else:
            context['error'] = 'Provide right Credentials'
            return render(request, 'auth/login.html', context)
    else:
        return render(request, 'auth/login.html', context)

@login_required(login_url="/login/")
def success(request):
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'auth/success.html', context)

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))

@login_required(login_url="/login/")
def employee_list(request):
    context = {}
    context['users'] = User.objects.all()
    context['title'] = "Employees"
    return render(request, 'employee/index.html', context)

@login_required(login_url="/login/")
def employee_details(request, id = None):
    context = {}
    u = get_object_or_404(User, id = id)
    if u:
        context['user'] = u
        return render(request, 'employee/details.html', context)
    else:
        return HttpResponse("Something went Wrong!")

@login_required(login_url="/login/")
def employee_add(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            u = user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
            #employee_list is name of url written in urls.py
            #reverse will convert the link to: employee/
        else:
            return render(request, 'employee/add.html', {"user_form" : user_form})
    else:
        user_form = UserForm()
        return render(request, 'employee/add.html', {"user_form" : user_form})

@login_required(login_url="/login/")
def employee_edit(request, id = None):
    user = get_object_or_404(User, id = id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance = user)  #if we don't pass instance, it will create new 
        # data
        if user_form.is_valid():
            u = user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/edit.html', {'user_form' : user_form})
    else:
        user_form = UserForm(instance = user)
        return render(request, "employee/edit.html", {'user_form': user_form})

@login_required(login_url="/login/")
def employee_delete(request, id = None):
    user = get_object_or_404(User, id = id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {}
        context['user'] = user
        return render(request, 'employee/delete.html', context)