from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.HelloView.as_view()),
    path('fetchbyifsc/', views.FetchByIFSC.as_view()),
    path('fetchbyname/', views.FetchByName.as_view()),
]