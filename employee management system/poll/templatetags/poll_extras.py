#make sure you restart the Django development server (or ensure it restarted itself) 
# every time you modify template tags. 

from django import template
from poll.models import Question
register = template.Library()

def upper(value):
    #Converts a string into all upper case
    return value.upper()

register.filter('upper', upper)
#whereevr this upper is used in html, this upper function will be called

@register.simple_tag
def recent_polls(n = 5, **kwargs):
    #return reecent polls
    name = kwargs.get("name", "No Argument is passed")
    print(name)
    questions = Question.objects.all().order_by('-created_at')
    return questions[0:n]