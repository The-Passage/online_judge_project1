from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('logout/', views.User_logout, name='logout'),
	path('signup/', views.register, name='signup'),
	path('login/', views.login, name='login'),
	path('signup/user_info', views.user_details, name='user_info'),
	path('password_change/', views.change_password, name='change_password'),
	path('user_profile/', views.user_details_view,name='user_details_view'),

	path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "registration/reset/reset_password.html"), name ='reset_password'),
  	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "registration/reset/password_reset_sent.html"), name ='password_reset_done'),
  	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "registration/reset/password_reset_form.html"), name ='password_reset_confirm'),
  	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "registration/reset/password_reset_done.html"), name ='password_reset_complete'),

]