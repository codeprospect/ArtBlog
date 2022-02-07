from django.contrib import admin
from .models import Post, Comment, Category
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
