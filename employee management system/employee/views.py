from django.shortcuts import render, get_object_or_404
from employee.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms
from employee.forms import UserForm
from django.urls import reverse
from django.http import Http404, HttpResponse

# Create your views here.

def employee_list(request):
    context = {}
    context['users'] = User.objects.all()
    context['title'] = "Employees"
    return render(request, 'employee/index.html', context)

def employee_details(request, id = None):
    context = {}
    context['user'] = get_object_or_404(User, id = id)
    return render(request, 'employee/details.html', context)

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

def employee_delete(request, id = None):
    user = get_object_or_404(User, id = id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {}
        context['user'] = user
        return render(request, 'employee/delete.html', context)