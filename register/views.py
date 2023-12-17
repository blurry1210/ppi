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


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Author, Post

@login_required
def profile(request):
    # Ensure we have an authenticated user
    if not request.user.is_authenticated:
        # Redirect to the login page or another appropriate page
        return redirect('login')

    # Retrieve the Author instance related to the current user
    try:
        user_author = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        # Handle the case where the Author instance does not exist
        # For example, create a new Author instance or redirect
        user_author = None  # Or handle it differently

    # Retrieve posts related to the author
    # Adjust the query if your Post model is linked to the Author model differently
    user_posts = Post.objects.filter(author=user_author)

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
    user_author, created = Author.objects.get_or_create(user=request.user)
    form = UpdateForm(request.POST or None, request.FILES or None, instance=user_author)
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

    