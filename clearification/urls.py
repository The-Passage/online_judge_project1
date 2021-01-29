from django.urls import path
from . import views

urlpatterns = [
    path('<int:contest_name>/', views.clearification, name='clearification'),
]