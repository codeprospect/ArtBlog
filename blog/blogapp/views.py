from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import PostSearchForm, PostCommentForm
from django.urls import reverse_lazy, reverse


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blogapp/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blogapp/home.html'
    context_object_name = 'posts'
    paginate_by = 4 #pagination


class UserPostListView(ListView):
    model = Post
    template_name = 'blogapp/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostCommentView(CreateView):
    model = Comment
    form_class = PostCommentForm
    template_name = 'blogapp/post_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk':self.kwargs['pk']})
    # success_url = reverse_lazy('post-detail')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

#The author is the current logged in user account
#A blog is automatically allocated to its logged in user, integrity check
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#Authors can only update their blogs
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' #redirect to homepage after deletion of a post

#Authors can only update their blogs
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blogapp/about.html', {'title': 'About'})


def post_detail(request, year, month, day, post):
    post = get_object_or_404 (Post, slug=post,
                                    status='published',
                                    publish_year=year,
                                    publish_month=month,
                                    publish_day=day)
    #active comments
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST) #Posted comment
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment = post #assigns current post to this comment
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render (request, 'blogapp/post_detail.html',
                    {'post': post,
                    'comments': comments,
                    'new_comment': new_comment,
                    'comment_form': comment_form})


# form = PostSearchForm(request.POST or None)
# queryset = Post.objects.all()
# context = {
#     "queryset": queryset,
# }
#
# if request.method == 'POST':
#     queryset = Post.objects.filter(author_icontains=form['author'].value(), title_icontains=form['title'].value())
#
#     context = {
#     "queryset": queryset,
#     }
