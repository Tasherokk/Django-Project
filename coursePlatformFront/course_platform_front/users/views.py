from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout

from .models import Profile


def homepage(request):
    return render(request, 'users/index.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("courses/")
    else:
        form = UserCreationForm()
    return render(request, "users/registration.html", {"form": form})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    return render(
        request,
        "users/profile.html",
        {
            "profile_user": user,
            "profile": profile,
        },
    )


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("users:profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "users/edit_profile.html", {"form": form})


def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("courses/")
    context = {'loginform': form}
    return render(request, 'users/my-login.html', context=context)


def user_logout(request):
    auth.logout(request)
    return redirect("")


@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'users/dashboard.html')
