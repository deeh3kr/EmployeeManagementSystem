from django.urls import path, include
from poll.views import *

urlpatterns = [
    path('', index, name = 'polls_list'),
    path('<int:id>/details/', details, name = 'poll_details'),
]