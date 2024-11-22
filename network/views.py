from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import *
from .forms import ProfileEditForm,LoginForm,RegisterForm
# from .utils import get_posts_dataframe, export_posts_to_csv, get_posts_as_html

def index(request):
    all_posts = Post.objects.all().order_by("-date_created")
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list("user", flat=True        )
        suggestions = (User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        )
    return render(request,"network/index.html",{"posts": posts,"suggestions": suggestions,"page": "all_posts","profile": False,},)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("index")
    else:
        form = LoginForm()
    
    context = {
        "form": form,
        "title": "Log in to Trendy",
        "button_label": "Log In",
        "show_signup_link": True,
    }
    return render(request, "network/layout2.html", context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegisterForm()
    context = {
        "form": form,
        "title": "Sign up for Trendy",
        "button_label": "Sign Up",
        "show_login_link": True,
    }
    return render(request, "network/layout2.html", context)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    all_posts = Post.objects.filter(creater=user).distinct().order_by("-date_created")
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)

    followers = Follower.objects.filter(user=user).values_list("followers", flat=True)
    following = Follower.objects.filter(followers=user).values_list("user", flat=True)

    is_follower = request.user in Follower.objects.filter(user=user).values_list("followers", flat=True)

    follower_count = followers.count()
    following_count = following.count()

    return render(
        request,
        "network/profile.html",
        {
            "username": user,
            "posts": posts,
            "page": 'profile',
            "posts_count": all_posts.count(),
            "followers": User.objects.filter(pk__in=followers),
            "following": User.objects.filter(pk__in=following),
            "is_follower": is_follower,
            "follower_count": follower_count,
            "following_count": following_count,
        },
    )


@login_required
def edit_profile(request, username):
    user_profile = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user_profile.username) 
    else:
        form = ProfileEditForm(instance=user_profile)

    context = {
        'form': form,
        'username': user_profile.username,
        "title": "Edit Profile",
        "button_label": "Save Changes",

    }
    return render(request, 'network/layout2.html', context)  


def following(request):
    if request.user.is_authenticated:
        following_user = Follower.objects.filter(followers=request.user).values("user")
        all_posts = Post.objects.filter(creater__in=following_user).order_by("-date_created")
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get("page")
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)
        followings = Follower.objects.filter(followers=request.user).values_list("user", flat=True)
        suggestions = (User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]) 
        return render(request,"network/index.html",{"posts": posts, "suggestions": suggestions, "page": "following"},)
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def create_post(request):
    if request.method == "POST":
        text = request.POST.get("text")
        pic = request.FILES.get("picture")
        try:
            Post.objects.create(creater=request.user, content_text=text, content_image=pic)
            return HttpResponseRedirect(reverse("index"))
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Method must be 'POST'")

@login_required
def toggle_like(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        if request.user in post.likers.all():
            post.likers.remove(request.user)
        else:
            post.likers.add(request.user)
        post.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
def follow(request, username):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = User.objects.get(username=username)
            print(f"...User: {user}...")
            print(f"...Follower: {request.user}...")
            try:
                (follower, created) = Follower.objects.get_or_create(user=user)
                follower.followers.add(request.user)
                follower.save()
                return HttpResponseRedirect(reverse("index"))
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            return JsonResponse({"error": "Method must be 'POST'"}, status=405)
    else:
        return HttpResponseRedirect(reverse("login"))
    

@csrf_exempt
def comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            comment_text = request.POST.get("comment_text")
            if comment_text:
                try:
                    new_comment = Comment.objects.create(post=post, commenter=request.user, comment_content=comment_text)
                    post.comment_count += 1
                    post.save()
                    comments = Comment.objects.filter(post=post).order_by('-comment_time')
                    return redirect("index")
                except Exception as e:
                    return HttpResponse(str(e), status=500)
        comments = Comment.objects.filter(post=post).order_by('-comment_time')
        return render(request, "network/index.html", {'post': post, 'comments': comments})
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def delete_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == "POST": 
            try:
                post = Post.objects.get(id=post_id)
                if request.user == post.creater:
                    post.delete() 
                    return redirect("profile", username=request.user.username)
                else:
                    return HttpResponse(status=403)
            except Post.DoesNotExist:
                return HttpResponse(status=404)
        else:
            return HttpResponse("Method must be 'POST'", status=405)
    else:
        return HttpResponse(status=401) 


def user_activity_chart(request):
    users = User.objects.all()
    user_data = []
    for user in users:
        post_count = Post.objects.filter(creater=user).count()
        follower_count = Follower.objects.filter(user=user).count()
        comment_count = Comment.objects.filter(commenter=user).count()

        user_data.append({
            "username": user.username,
            "posts": post_count,
            "followers": follower_count,
            "comments": comment_count,
        })

    context = {
        'user_data': user_data
    }
    return render(request, 'network/user_activity_chart.html', context)