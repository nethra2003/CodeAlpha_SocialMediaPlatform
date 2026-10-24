from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile_view, name="profile"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("profile/edit/", views.edit_profile_view, name="edit_profile"),
    path("profile/<str:username>/", views.profile_view, name="user_profile"),

    path("feed/", views.feed_view, name="feed"),
    path("post/create/", views.create_post_view, name="create_post"),
    path(
        "post/<int:post_id>/delete/",
        views.delete_post_view,
        name="delete_post"
    ),
    path(
    "post/<int:post_id>/comment/",
    views.add_comment_view,
    name="add_comment"
    ),
    path(
    "post/<int:post_id>/like/",
    views.toggle_like_view,
    name="toggle_like"
    ),
    path(
    "follow/<str:username>/",
    views.toggle_follow_view,
    name="toggle_follow"
    ),
    path(
    "discover/",
    views.discover_users_view,
    name="discover_users"
    ),
]

