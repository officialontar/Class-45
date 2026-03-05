from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'accounts/index.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!!")
            return redirect('register')
        
        if User.objects.filter(user_name = user_name).exists():
            messages.error(request, "Username already exists!!")
            return redirect('register')
        
        if User.objects.filter(email = email).exists():
            messages.error(request, "Email already exists!!")
            return redirect('register')
        
        # Create user with hased password for using create_user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=user_name,
            email=email,
            password=password
        )
        user.first_name = first_name
        user.last_name = last_name
        
        user.save()
        messages.success(request, f"Account for {user_name} created successfully!")
        return redirect('login')

    return render(request, 'accounts/register.html')

def login_view(request):

    if request.method == 'POST':
        username_or_email_or_phone_number = request.POST.get('username_or_email_or_phone_number')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username = username_or_email_or_phone_number)
            user_name = user_obj.username
            
        except User.DoesNotExist:
                user_name = username_or_email_or_phone_number
                
        user = authenticate(request, username = username_or_email_or_phone_number, password = password)

        if user is not None:
            login(request, user)

            messages.success(request, f"Welcome back {user.username} Login Successful!")

            return redirect('home')
        
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'accounts/login.html')

def logout_view(request):

    logout(request)
    messages.success(request, "Logout successful!")
    return redirect('login')

def profile(request):
    
    return render(request, 'accounts/profile.html')
