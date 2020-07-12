from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    context['title'] = 'polls'
    return render(request, 'polls/index.html', context)

