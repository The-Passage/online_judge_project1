from django.urls import path
from . import views

urlpatterns = [
	path('contestlist/', views.contest_list, name='contest_list'),
	path('<int:pk>/', views.contest_info, name='contest_info'),
	path('<int:pk>/dashboard/', views.contest_dashboard, name='contest_dashboard'),
	path('<int:pk>/contest_pass/', views.contest_pass_test, name='contest_pass_test'),
	path('<int:pk>/dashboard/<int:problem_id>', views.contest_show_problem, name='contest_show_problem'),
	path('<int:pk>/submission/', views.contest_individual_submission, name='contest_individual_submission'),
	path('<int:pk>/standing/', views.contest_standing, name='contest_standing'),
	path('contest_standing_server/<int:pk>/', views.contest_standing_server, name='contest_standing_server'),
]