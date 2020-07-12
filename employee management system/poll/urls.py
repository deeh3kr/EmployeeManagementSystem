from django.urls import path, include
from poll.views import index

urlpatterns = [
    path('', index, name = 'polls_list'),
]