from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from main.models import Author, Post
from register.forms import UpdateForm
from django.contrib.auth import logout as lt
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def view_profile(request, username):
    if request.user.username == username:
        # Display the profile of the logged-in user
        user_profile = get_object_or_404(Author, user=request.user)
    else:
        # Display the profile of other users
        user_profile = get_object_or_404(Author, user__username=username)

    context = {'user_profile': user_profile}
    return render(request, 'profile.html', context)


def profile(request):
    user_author = Author.objects.get(user=request.user)
    user_posts = Post.objects.filter(user=user_author)

    context = {
        'user_author': user_author,
        'user_posts': user_posts,
        'title': 'F1 ZONE: Profile',
    }

    return render(request, 'profile.html', context)

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
        "title": "Sign up",
    })
    return render(request, "register/signup.html", context)

def signin(request):
    context = {'key': 'value'}
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
        "title": "Sign in",
    })
    return render(request, "register/signin.html", context)

@login_required
def update_profile(request):
    context = {}
    user = request.user 
    form = UpdateForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            update_profile = form.save(commit=False)
            update_profile.user = user
            update_profile.save()
            return redirect("home")

    context.update({
        "form": form,
        "title": "Update Profile",
    })
    return render(request, "register/update.html", context)

@login_required
def logout(request):
    lt(request)
    return redirect("home")

    