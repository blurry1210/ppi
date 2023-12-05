
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
    user_author = Author.objects.get(user=request.user)
    user_posts = Post.objects.filter(user=user_author)

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

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)
    
    if request.method == "POST":
        if "comment-form" in request.POST:
            comment_content = request.POST.get("comment")
            new_comment, created = Comment.objects.get_or_create(user=author, content=comment_content)
            post.comments.add(new_comment)

        elif "reply-form" in request.POST:
            reply_content = request.POST.get("reply")
            commenr_id = request.POST.get("comment-id")
            comment_obj = Comment.objects.get(id=commenr_id)
            new_reply, created = Reply.objects.get_or_create(user=author, content=reply_content)
            comment_obj.replies.add(new_reply)

        return redirect("detail", slug=slug)

    # Fetch comments related to the post's forum
    forum_comments = Comment.objects.filter(post__categories__in=post.categories.all())

    context = {
        "post": post,
        "forum_comments": forum_comments,
        "title": "F1 ZONE: " + post.title,
    }
    update_views(request, post)

    return render(request, "detail.html", context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category).order_by('-date')
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Print category information
    print(f"Category: {category}")

    # Print posts to the terminal
    print(f"Posts in category '{category}':")
    for post in posts:
        print(f"- {post.title}")

    context = {
        "posts": posts,
        "forum": category,
        "title": "F1 ZONE: Posts"
    }

    return render(request, "posts.html", context)

@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()

            # Get the selected category (assuming it's a ForeignKey)
            selected_category = form.cleaned_data.get('categories').first()

            # Check if a category was selected before associating it with the post
            if selected_category:
                new_post.categories.add(selected_category)

            return redirect("home")

    context.update({
        "form": form,
        "title": "F1 ZONE: Create New Post",
        "categories": Category.objects.all(),
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