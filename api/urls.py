from django.conf.urls import url

from . import views

urlpatterns = [
    url('ExampleView/', views.ExampleView.as_view(), name='ExampleView'),
    url('user/', views.UserListView.as_view(), name='user'),
    url("checkUser/", views.checkUser, name='checkUser'),
    url("login/", views.login, name='login')
]
