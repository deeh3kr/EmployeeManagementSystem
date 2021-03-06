from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.db.models import Q

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import action
from poll.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from ems.decorators import admin_hr_required, admin_only
from poll.forms import *

# Create your views here.

class PollView(View):
    decorators = [login_required, admin_hr_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Question, id=id)
            poll_form = PollForm(instance=question)
            choices = question.choice_set.all()
            choice_forms = [ChoiceForm(prefix=str(
                choice.id), instance=choice) for choice in choices]
            template = 'polls/edit_poll.html'
        else:
            poll_form = PollForm(instance=Question())
            choice_forms = [ChoiceForm(prefix=str(
                x), instance=Choice()) for x in range(3)]
            template = 'polls/new_poll.html'
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        context = {}
        if id:
            return self.put(request, id)
        poll_form = PollForm(request.POST, instance=Question())
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return HttpResponseRedirect('/polls/list/')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/new_poll.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        context = {}
        question = get_object_or_404(Question, id=id)
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return redirect('polls_list')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/edit_poll.html', context)

    @method_decorator(decorators)
    def delete(self, request, id=None):
        question = get_object_or_404(Question)
        question.delete()
        return redirect('polls_list')

@login_required(login_url="/login/")
def poll_delete(request, id = None):
    poll = get_object_or_404(Question, id = id)
    if request.method == 'POST':
        poll.delete()
        return HttpResponseRedirect(reverse('polls_list'))
    else:
        context = {}
        context['poll'] = poll
        return render(request, 'polls/delete.html', context)


@login_required(login_url="/login/")
def index(request):
    #context is list of variables to be passed to html pages
    questions = Question.objects.all()
    context = {}
    context['title'] = 'polls'
    context['questions'] = questions
    return render(request, 'polls/index.html', context)

@login_required(login_url="/login/")
def details(request, id = None):
    #context is list of variables to be passed to html pages
    try:
        question = Question.objects.get(id = id)
    except:
        raise Http404
    context = {}
    context['question'] = question
    return render(request, 'polls/details.html', context)

@login_required(login_url="/login/")
def poll(request, id = None):
    try:
        question = Question.objects.get(id = id)
    except:
        raise Http404

    context = {}
    context['question'] = question

    if request.method == "GET":
        return render(request, 'polls/poll.html', context)

    if request.method == 'POST':
        user_id = 1
        data = request.POST
        #print (data)
        # user is a foriegn key, so you can access it's other field by __ and it's id by _
        ret = Answer.objects.create(user_id = user_id, choice_id = data['choice'])  # data['choice'] because in poll.html
        # we named radio button with choice
        if ret:
            #return HttpResponse("Your vote is registered")
            return render(request, 'polls/details.html', context) 
        else:
            return HttpResponse("Something went Wrong!")

@login_required(login_url="/login/")
def vote_poll(request, id=None):
    context = {}
    try:
        question = Question.objects.get(id=id)
    except:
        raise Http404
    context["question"] = question

    if request.method == "POST":
        user_id = 1
        print(request.POST)
        data = request.POST
        ret = Answer.objects.create(user_id=user_id, choice_id=data['choice'])
        if ret:
            return HttpResponseRedirect(reverse('poll_details', args=[question.id]))
        else:
            context["error"] = "Your vote is not done successfully"
            return render(request, 'polls/poll.html', context)
    else:
        return render(request, 'polls/poll.html', context)