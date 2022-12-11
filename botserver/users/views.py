from django.shortcuts import render
from django.views import View
from .forms import CustomUserCreationForm
from django.shortcuts import redirect, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


class CreateUserView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "users/create.html", context={"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index_url")
        else:
            return render(request, "users/create.html", context={"form": form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "users/login.html", context={"form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index_url")
        return render(request, "users/login.html", context={"form": form})
