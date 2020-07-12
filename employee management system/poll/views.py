from django.shortcuts import render
from poll.models import *
from django.http import Http404, HttpResponse

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

def poll(request, id = None):
    try:
        question = Question.objects.get(id = id)
    except:
        raise Http404
    if request.method == "GET":
        context = {}
        context['question'] = question
        return render(request, 'polls/poll.html', context)

    if request.method == 'POST':
        user_id = 1
        data = request.POST
        #print (data)
        # user is a foriegn key, so you can access it's other field by __ and it's id by _
        ret = Answer.objects.create(user_id = user_id, choice_id = data['choice'])  # data['choice'] because in poll.html
        # we named radio button with choice
        if ret:
            return HttpResponse("Your vote is registered")
        else:
            return HttpResponse("Something went Wrong!")
