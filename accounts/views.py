from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    return render(request, 'accounts/index.html')


# ✅ If user already logged in, block register page
def register(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in. Logout first to create a new account.")
        return redirect('profile', request.user.username)

    if request.method == "POST":
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        image = request.FILES.get('profile_image')

        if image:
            if image.size > 10 * 1024 * 1024:
                messages.error(request, "Image size must be under 10MB")
                return redirect('register')


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


# ✅ If user already logged in, block login page
def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('profile', request.user.username)

    if request.method == "POST":
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=username_or_email)
            user_name = user_obj.username
        except User.DoesNotExist:
            user_name = username_or_email

        user = authenticate(request, username=user_name, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credential!')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('login')


# ✅ Profile: login required + block others profile if you want
@login_required
def profile(request, user_name):
    # 🔒 If someone tries /profile/otheruser/ while logged in, redirect to own profile
    if user_name != request.user.username:
        messages.info(request, "You can only access your own profile.")
        return redirect('profile', request.user.username)

    user = get_object_or_404(User, username=user_name)

    context = {
        'user_profile': user
    }
    
    return render(request, 'accounts/profile.html', context)