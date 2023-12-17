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
        "title": "OZONE forum app"
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
        "title": f"OZONE: {post.title}",
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
        "title": "OZONE: Posts"
    }

    return render(request, "posts.html", context)


@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("\n\n its valid")
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            form.save_m2m()
            return redirect("home")
    context.update({
        "form": form,
        "title": "OZONE: Create New Post"
    })
    return render(request, "create_post.html", context)

def latest_posts(request):
    posts = Post.objects.all().filter(approved=True)[:10]
    context = {
        "posts":posts,
        "title": "OZONE: Latest 10 Posts"
    }

    return render(request, "latest-posts.html", context)

def search_result(request):

    return render(request, "search.html")