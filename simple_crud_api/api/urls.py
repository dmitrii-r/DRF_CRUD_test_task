from django.urls import path

from api.views import api_posts, api_posts_detail

app_name = "api"

urlpatterns = [
    path("posts/", api_posts, name="api_posts"),
    path("posts/<int:pk>/", api_posts_detail, name="api_posts_detail"),
]
