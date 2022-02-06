from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, PostCommentView, LikeView, PostCategoryView
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name = 'blogapp-home'),
    path('user/<str:username>', UserPostListView.as_view(), name = 'user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/category/', PostCategoryView.as_view(), name = 'post-category'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('post/<int:pk>/comment/', PostCommentView.as_view(), name = 'post-comment'),
    path('post/like/<int:pk>/', LikeView, name = 'post-like'),
    path('about/', views.about, name = 'blogapp-about'),
]
