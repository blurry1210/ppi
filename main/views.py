from django.shortcuts import redirect, render, get_object_or_404
from .models import Author, Category, Post, Comment, Reply
from .utils import update_views
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Comment, Reply, Author
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def profile_view(request):
    # Fetch the Author instance related to the current user
    try:
        user_author = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        # Handle the case where the Author instance does not exist
        user_author = None

    # Fetch posts related to the author
    user_posts = Post.objects.filter(user=user_author).order_by('-date') if user_author else []

    context = {
        'user_author': user_author,
        'user_posts': user_posts,
    }

    return render(request, 'profile.html', context)

def home(request):
    # Initialize empty querysets
    forums = Category.objects.none()
    last_post = None

    # Check if the user has an 'author' profile and chosen categories
    if hasattr(request.user, 'author'):
        chosen_categories = request.user.author.chosen_categories.all()
        if chosen_categories.exists():
            forums = chosen_categories
            num_posts = Post.objects.filter(categories__in=chosen_categories).count()
            try:
                last_post = Post.objects.filter(categories__in=chosen_categories).latest('date')
            except Post.DoesNotExist:
                last_post = None
        else:
            num_posts = 0
    else:
        num_posts = 0

    num_users = User.objects.all().count()
    num_categories = forums.count()

    context = {
        "forums": forums,
        "num_posts": num_posts,
        "num_users": num_users,
        "num_categories": num_categories,
        "last_post": last_post,
        "title": "F1 ZONE forum app"
    }
    return render(request, "forums.html", context)

@login_required
def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Check if the user has an associated author profile and create one if not
    author, created = Author.objects.get_or_create(user=request.user)

    # Handling comments
    if request.method == "POST" and "comment-form" in request.POST:
        comment_content = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(
            user=author, content=comment_content, post=post
        )
        if created:
            post.comments.add(new_comment)
            messages.success(request, "Your comment has been added.")

    # Handling replies
    if request.method == "POST" and "reply-form" in request.POST:
        reply_content = request.POST.get("reply")
        comment_id = request.POST.get("comment-id")
        comment_obj = get_object_or_404(Comment, id=comment_id)
        new_reply, created = Reply.objects.get_or_create(
            user=author, content=reply_content, comment=comment_obj
        )
        if created:
            comment_obj.replies.add(new_reply)
            messages.success(request, "Your reply has been posted.")

    if request.method == "POST":
        return redirect('detail', slug=post.slug)

    comments = post.comments.prefetch_related('replies').all()

    context = {
        "post": post,
        "comments": comments,
        "title": "F1 ZONE: {post.title}",
    }
    update_views(request, post)

    return render(request, "detail.html", context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 

    context = {
        "posts":posts,
        "forum": category,
        "title": "F1 ZONE: Posts"
    }

    return render(request, "posts.html", context)


@login_required
def create_post(request):
    context = {}
    if request.method == "POST":
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user.author
            new_post.save()
            form.save_m2m()
            return redirect("home")
    else:
        form = PostForm(user=request.user)

    context.update({
        "form": form,
        "title": "F1 ZONE: Create New Post"
    })
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

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.user.user:
        raise PermissionDenied

    post.delete()
    # Redirect to a success page or home page
    return redirect('home')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user.user:
        raise PermissionDenied

    comment.delete()
    return redirect('home')

@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    if request.user != reply.user.user:
        raise PermissionDenied

    reply.delete()
    return redirect('home')