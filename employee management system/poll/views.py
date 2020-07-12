from django.shortcuts import render
from poll.models import *
from django.http import Http404

# Create your views here.

def index(request):
    #context is list of variables to be passed to html pages
    questions = Question.objects.all()
    context = {}
    context['title'] = 'polls'
    context['questions'] = questions
    return render(request, 'polls/index.html', context)

def details(request, id = None):
    #context is list of variables to be passed to html pages
    try:
        question = Question.objects.get(id = id)
    except:
        raise Http404
    context = {}
    context['question'] = question
    return render(request, 'polls/details.html', context)
