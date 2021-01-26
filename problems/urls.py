from django.urls import path
from . import views

urlpatterns = [
	path('problemlist/', views.problem_list, name='problem_list'),
	path('<int:pk>/', views.show_problem, name='show_problem'),
	path('submission/', views.show_submission, name='show_submission'),
	path('submission/<int:pk>/', views.individual_submission, name='individual_submission'),
]