from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.
def home(request):
    
    return render(request, 'accounts/index.html')


def register(request):

    if request.method == "POST":
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Password do not match!')
            return redirect('register')

        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'Username already exist!')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')

        user = User.objects.create_user(
            username=user_name,
            email=email,
            password=password
        )

        user.first_name = firstname
        user.last_name = lastname
        user.save()

        messages.success(request, 'Account created successfully.')
        return redirect('login')

    return render(request, 'accounts/register.html')

def login_view(request):
    
    if request.method == "POST":
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email = username_or_email)
            user_name = user_obj.username
             
        except User.DoesNotExist:
            user_name = username_or_email

        user = authenticate(request, username = user_name, password = password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfull')
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid Credential!')
            return redirect('login')
        
    return render(request, 'accounts/login.html')


def logout_view(request):
    
    logout(request)
    messages.success(request, 'Logout Successfull')
    
    return redirect('login')
    
@login_required
def profile(request, user_name):

    user = get_object_or_404(User, username=user_name)

    context = {
        'user_profile': user
    }

    return render(request, 'accounts/profile.html', context)