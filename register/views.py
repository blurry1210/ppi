from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from register.forms import UpdateForm
from django.contrib.auth import logout as lt
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UpdateProfileForm
from  main.models import Author, Category, Post


#usernames = [user.username for user in User.objects.all()]

def signup(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("update_profile")
    context.update({
        "form":form, 
        "title": "Signup",
    })
    return render(request, "register/signup.html", context)

def signin(request):
    context = {}
    form = AuthenticationForm(request, data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    context.update({
        "form": form,
        "title": "Signin",
    })
    return render(request, "register/signin.html", context)

@login_required
def update_profile(request):
    context = {}
    user = request.user
    author, created = Author.objects.get_or_create(user=user)

    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            update_profile = form.save(commit=False)
            update_profile.user = user
            update_profile.save()
            # This line ensures that the selected categories are saved after the main object
            update_profile.chosen_categories.set(form.cleaned_data['chosen_categories'])
            return redirect("home")
    else:
        form = UpdateProfileForm(instance=author)

    context.update({
        "form": form,
        "title": "Update Profile",
    })
    return render(request, "register/update.html", context)

@login_required
def logout(request):
    lt(request)
    return redirect("home")