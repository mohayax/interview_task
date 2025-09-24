from django.urls import path
from .views import BlogView, BlogDetailView, BlogLikeView, CommentView, CommentDetailView

urlpatterns = [
    path("get-create", BlogView.as_view(), name="get_create_blog"),
    path("<uuid:id>/like", BlogLikeView.as_view(), name="blog_like"),
    path("<uuid:id>", BlogDetailView.as_view(), name="blog_details"),
    path("make-comment/<uuid:id>", CommentView.as_view(), name="comment"),
    path("comment/<uuid:id>", CommentDetailView.as_view(), name="comment_detail"),
]

