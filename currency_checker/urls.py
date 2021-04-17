from django.urls import path
from currency_checker import views

urlpatterns = [
    path('',views.index,name='index')
]