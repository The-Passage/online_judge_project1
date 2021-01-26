from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserDetails
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import EditItemForm
from .forms import ItemForm
import traceback
import sys

# Create your views here.

def User_logout(request):
    try:
        logout(request)
        return HttpResponseRedirect(reverse('home'))
    except:
        return render(request, '404.html')

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    try:
        if request.method == 'POST':
            error = {}

            user_name = request.POST['user_name']
            email = request.POST['email']
            hashed_password = request.POST['password']
            confirmed_hashed_password = request.POST['confirm_password']

            try:
                validate_email(email)
            except:
                error['email_error'] = "Bad email"
            if ' ' in user_name:
                error['user_error1'] = "invalid username"
            if User.objects.filter(username=user_name).count() != 0:
                error['user_error'] = "Username Already Exists"
            if User.objects.filter(email=email).count() != 0:
                error['email_error'] = "Email Already Exists"
            if hashed_password != confirmed_hashed_password:
                error['password_missmatch'] = "Passwords Didn't Match"

            if len(error):
                return render(request, 'registration/signup.html', error)

            u = User.objects.create_user(username=user_name,email=email, password=hashed_password)
            u.save()
            currentuser = authenticate(username=user_name, password=hashed_password)
            instance = UserDetails(u_name=currentuser)
            instance.save()
            if currentuser:
                if currentuser.is_authenticated:
                    #return HttpResponseRedirect(reverse('login'))
                    auth_login(request, currentuser)
                    return render(request, 'registration/signup_details.html')
                    #usr = currentuser.objects.all()
                    #return HttpResponseRedirect(reverse('user_details', kwargs={'pk': usr}))
                else:
                    return HttpResponse("Your Account is not active")
            else:
                HttpResponse("Something Wrong Happened")

        else:
            return render(request, 'registration/signup.html')
    except:
        return render(request, '404.html')

def user_details(request):
    try:
        print("hii")
        if request.method == 'POST':
            p = UserDetails.objects.get(u_name=request.user)
            form = ItemForm(request.POST, instance=p)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, '404.html')
            #gender = request.POST.get('gender')
            #profession = request.POST.get('profession')
            #institute = request.POST.get('institute')
            #institute_id = request.POST.get('institute_id')
            #first_name = request.POST['first_name']
            #last_name = request.POST['last_name']
            #instance = UserDetails(u_name=request.user, gender=gender, profession=profession, institute=institute, institute_id=institute_id, first_name=first_name, last_name=last_name)
            #instance.save()
            #return HttpResponseRedirect(reverse('home'))
        else:
            print("hi")
            return render(request, 'registration/signup_details.html')
    except Exception:
        traceback.print_exc()
        return render(request, '404.html')

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            error = {}
            if user:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    error['message'] = "Disabled Account"
                    return render(request, 'registration/login.html', error)
            else:
                error['message'] = "Invalid Username or Password"
                return render(request, 'registration/login.html', error)
        else:
            return render(request, 'registration/login.html')
    except:
        return render(request, '404.html')

def change_password(request):
    try:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                logout(request)
                return redirect('login')
            else:
                messages.error(request, 'error')
        else:
            form = PasswordChangeForm(request.user)

        return render(request, 'registration/change_password.html')
    except:
        return render(request, '404.html')

def user_details_view(request):
    try:
        p = UserDetails.objects.get(u_name=request.user)
        context = {}
        context['detail'] = p
        if request.method == 'POST':
            print("paisi")
            form = EditItemForm(request.POST, instance=p)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, '404.html')
        else:
            return render(request, 'registration/user_profile.html', context)
    except Exception:
        traceback.print_exc()
        return render(request, '404.html')

def csrf_failure(request, reason=""):
    return render(request, '404.html')