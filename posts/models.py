from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=70)
    content = models.TextField()
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/media/uploads/', null=True, blank=True)

    def ava_rating(self):
        ratings = self.comments.all()
        print(ratings,"**8")
        if ratings:
            return sum([rating.value for rating in ratings]) / len(ratings)
        return 0


    def __str__(self):
        return self.title



star = (
    ("⭐","⭐"),
    ("⭐⭐","⭐⭐"),
    ("⭐⭐⭐","⭐⭐⭐"),
    ("⭐⭐⭐⭐","⭐⭐⭐⭐"),
    ("⭐⭐⭐⭐⭐","⭐⭐⭐⭐⭐"),
)

    
class Commnet(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    review = models.CharField(max_length = 10, choices = star, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comments By {self.body}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)