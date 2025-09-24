from django.urls import path
from .views import SignUp, UserList

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('get-users', UserList.as_view(), name='users'),
]
