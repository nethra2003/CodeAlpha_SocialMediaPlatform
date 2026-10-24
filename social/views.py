from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Like, Follow
from .forms import RegisterForm, ProfileUpdateForm, PostForm, CommentForm
from django.db import models

def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Your account has been created successfully!"
            )
            return redirect("profile")
    else:
        form = RegisterForm()

    return render(request, "social/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("feed")

        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "social/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have logged out.")
        return redirect("login")

    return redirect("profile")


@login_required
def profile_view(request, username=None):
    if username is None:
        profile_user = request.user
    else:
        try:
            profile_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("profile")

    profile, _ = Profile.objects.get_or_create(
        user=profile_user
    )

    posts = profile_user.posts.order_by("-created_at")

    is_following = profile_user.followers.filter(
        follower=request.user
    ).exists()

    context = {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
        "follower_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
        "is_following": is_following,
    }

    return render(
        request,
        "social/profile.html",
        context
    )

@login_required
def edit_profile_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Profile updated successfully!"
            )
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(
        request,
        "social/edit_profile.html",
        {"form": form}
    )


@login_required
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(
                request,
                "Your post was published successfully!"
            )
            return redirect("feed")

        messages.error(
            request,
            "Please correct the errors below before publishing."
        )
    else:
        form = PostForm()

    return render(
        request,
        "social/create_post.html",
        {"form": form}
    )


@login_required
def delete_post_view(request, post_id):
    if request.method == "POST":
        post = Post.objects.filter(
            id=post_id,
            author=request.user
        ).first()

        if post:
            post.delete()
            messages.success(request, "Post deleted successfully!")
        else:
            messages.error(
                request,
                "Post not found or you cannot delete this post."
            )

    return redirect("feed")


@login_required
def feed_view(request):
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list("followed_id", flat=True)

    posts = Post.objects.filter(
        models.Q(author=request.user) |
        models.Q(author_id__in=following_ids)
    ).select_related(
        "author"
    ).prefetch_related(
        "likes",
        "comments__author"
    ).order_by("-created_at")

    liked_post_ids = set(
        Like.objects.filter(
            user=request.user
        ).values_list("post_id", flat=True)
    )

    return render(
        request,
        "social/feed.html",
        {
            "posts": posts,
            "liked_post_ids": liked_post_ids,
        }
    )


@login_required
def add_comment_view(request, post_id):
    if request.method == "POST":
        post = Post.objects.filter(id=post_id).first()

        if post is None:
            messages.error(request, "Post not found.")
            return redirect("feed")

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            messages.success(request, "Comment added successfully.")
        else:
            messages.error(
                request,
                "Please enter a valid comment."
            )

    return redirect("feed")


@login_required
def toggle_like_view(request, post_id):
    if request.method != "POST":
        return redirect("feed")

    post = Post.objects.filter(id=post_id).first()

    if post is None:
        messages.error(request, "Post not found.")
        return redirect("feed")

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        like.delete()
        messages.success(request, "You unliked this post.")
    else:
        messages.success(request, "You liked this post.")

    return redirect("feed")


@login_required
def toggle_follow_view(request, username):
    if request.method != "POST":
        return redirect("user_profile", username=username)

    target_user = User.objects.filter(
        username=username
    ).first()

    if target_user is None:
        messages.error(request, "User not found.")
        return redirect("feed")

    if target_user == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("profile")

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        followed=target_user
    )

    if created:
        messages.success(
            request,
            f"You are now following {target_user.username}."
        )
    else:
        follow.delete()
        messages.success(
            request,
            f"You unfollowed {target_user.username}."
        )

    return redirect("user_profile", username=target_user.username)



@login_required
def discover_users_view(request):
    search_query = request.GET.get("q", "").strip()

    users = User.objects.exclude(
        id=request.user.id
    )

    if search_query:
        users = users.filter(
            username__icontains=search_query
        )

    users = users.order_by("username")

    following_ids = set(
        Follow.objects.filter(
            follower=request.user
        ).values_list("followed_id", flat=True)
    )

    return render(
        request,
        "social/discover_users.html",
        {
            "users": users,
            "following_ids": following_ids,
            "search_query": search_query,
        }
    )
