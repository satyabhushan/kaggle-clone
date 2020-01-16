from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required



def register_view(request):
    print(request.user.id)
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserRegisterForm()
    return render(request, "main/register.html", {"form": form})


def login_view(request):
    username = password = ""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/")
    return render(request, "main/login.html")


@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect("/register")

