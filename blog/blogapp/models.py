from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import readtime

class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('post-detail')


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=255,default='Personal', null=True)
    snippet = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    content = models.TextField()
    date = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, blank=True,related_name="blog_posts")

    # Readtime function
    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result.text

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    # email = models.EmailField()
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    # active = models.BooleanField(default=True)

    class Meta:
        ordering = ('date_added',)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

    # def __str__(self):
    #     return f'Comment by {self.name} on {self.post}'
