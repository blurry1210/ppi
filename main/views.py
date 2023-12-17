
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Author, Category, Post, Comment, Reply, Forum
from .utils import update_views
from .forms import PostForm
from django.shortcuts import get_object_or_404

@login_required
def profile(request):
    try:
        user_author = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        user_author = None  # Handle the case when the author does not exist

    user_posts = Post.objects.filter(user=user_author) if user_author else []

    context = {
        'user_author': user_author,
        'user_posts': user_posts,
        'title': 'F1 ZONE: Profile',
    }
    return render(request, 'profile.html', context)

def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'user': user})


def home(request):
    forums = Category.objects.all()
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = forums.count()
    try:
        last_post = Post.objects.latest("date")
    except:
        last_post = []

    context = {
        "forums":forums,
        "num_posts":num_posts,
        "num_users":num_users,
        "num_categories":num_categories,
        "last_post":last_post,
        "title": "F1 ZONE : Home"
    }
    return render(request, "forums.html", context)

def posts(request, slug):
    # Get the category object based on the slug
    category = get_object_or_404(Category, slug=slug)
    
    # Get all posts that belong to this category and are approved
    posts_in_category = Post.objects.filter(categories=category, approved=True).order_by('-date')

    # Set up pagination if needed, here we are showing all posts without pagination
    # If you wish to add pagination, refer to the example you provided earlier

    context = {
        'posts': posts_in_category,  # The posts to display
        'forum': category,  # The category (forum) these posts belong to
        'title': f'F1 ZONE: {category.title} Posts',  # The page title
    }
    
    # Render the 'posts.html' template with the posts and category information
    return render(request, 'posts.html', context)

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    author = None
    if request.user.is_authenticated:
        author, _ = Author.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        if "comment-form" in request.POST and author:
            comment_content = request.POST.get("comment")
            new_comment, created = Comment.objects.get_or_create(
                user=author, 
                content=comment_content,
                post=post  # Make sure you associate the comment with the post
            )
            if created:
                post.comments.add(new_comment)

        elif "reply-form" in request.POST and author:
            reply_content = request.POST.get("reply")
            comment_id = request.POST.get("comment-id")
            comment_obj = Comment.objects.get(id=comment_id)
            new_reply, created = Reply.objects.get_or_create(
                user=author, 
                content=reply_content,
                comment=comment_obj  # Associate the reply with the comment
            )
            if created:
                comment_obj.replies.add(new_reply)

        return redirect('post_detail', slug=slug)  # Make sure 'post_detail' is the correct URL name

    forum_comments = Comment.objects.filter(post=post)

    context = {
        "post": post,
        "forum_comments": forum_comments,
        "title": f"F1 ZONE: {post.title}",
    }
    update_views(request, post)

    return render(request, "detail.html", context)

@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST" and form.is_valid():
        # Get the author corresponding to the logged-in user
        author, created = Author.objects.get_or_create(user=request.user)
        
        # Create a new post instance, but don't save it to the database yet
        new_post = form.save(commit=False)

        # Assign the logged-in user to the user field of the post
        new_post.user = request.user  # Make sure this matches the field in your Post model

        # Save the post to the database
        new_post.save()

        # If your Post model has any many-to-many fields, save them too
        form.save_m2m()

        return redirect("home")

    context = {
        "form": form,
        "title": "Create New Post",
    }
    return render(request, "create_post.html", context)




def latest_posts(request):
    posts = Post.objects.all().filter(approved=True)[:10]
    context = {
        "posts":posts,
        "title": "F1 ZONE: Latest 10 Posts"
    }

    return render(request, "latest-posts.html", context)

def search_result(request):

    return render(request, "search.html")