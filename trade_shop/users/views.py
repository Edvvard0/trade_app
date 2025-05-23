from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import UserLoginForm


@login_required
def profile(requests):
    user = requests.user
    return render(requests, "users/profile.html", context={"user": user})


def login_user(requests):
    if requests.method == "POST":
        form = UserLoginForm(requests.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(requests,
                                username=cd["username"],
                                password=cd["password"])

            if user and user.is_active:
                login(requests, user)
                return HttpResponseRedirect(reverse("profile"))

    else:
        form = UserLoginForm()

    return render(requests, "users/login.html", context={"form": form})


def logout_user(requests):
    logout(requests)
    return HttpResponseRedirect(reverse("login"))