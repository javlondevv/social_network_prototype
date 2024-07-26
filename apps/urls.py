from django.urls import path

from apps import views
from apps.views import (LoginPageView, NotificationsView, PostCreateView,
                        PostDetailView, PostListView, ProfileView,
                        RegisterPageView, UserLogoutView, index_page_view)

urlpatterns = [
    path("", index_page_view, name="index"),
    path("profile/", RegisterPageView.as_view(), name="register"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("posts/create/", PostCreateView.as_view(), name="create_post"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/like/<int:pk>/", views.BlogPostLike, name="blogpost_like"),
    path("logout/", UserLogoutView.as_view(next_page="login"), name="logout"),
    path("profile-update/", ProfileView.as_view(), name="profile"),
    path("notifications/", NotificationsView.as_view(), name="notifications"),
]
