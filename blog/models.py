from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
import uuid


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    cover_photo = models.ImageField(upload_to="blog_covers/", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    likes = models.ManyToManyField(User, related_name="liked_blogs", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)     

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.name} on {self.blog.title}"
