# use of this context processor is to calculate some values in every request.
# whenever you visit any page, this value will be calculated

from poll.models import Question

def polls_count(request):
    count = Question.objects.count()
    return {'polls_count': count}