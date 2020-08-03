from django.urls import path, include
from poll.views import *

urlpatterns = [
    path('add/', PollView.as_view(), name='poll_add'),
    path('<int:id>/edit/', PollView.as_view(), name='poll_edit'),
   # path('<int:id>/delete/', PollView.as_view(), name='poll_delete'),
    path('<int:id>/delete/', poll_delete, name = 'poll_delete'),
    path('list/', index, name = 'polls_list'),
    path('<int:id>/details/', details, name = 'poll_details'),
    path('<int:id>/', vote_poll, name="poll_vote")
    #path('<int:id>/', poll, name = 'single_poll'),
]