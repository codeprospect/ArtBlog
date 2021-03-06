from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Category
from .forms import PostForm, PostSearchForm, PostCommentForm, PostContactForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blogapp/home.html', context)

#Like Dislike Features
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    # liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        # liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class PostListView(ListView):
    model = Post
    template_name = 'blogapp/home.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 4 #pagination

class PostOriginalView(ListView):
    model = Post
    template_name = 'blogapp/originals.html'
    context_object_name = 'posts'
    ordering = ['date']
    paginate_by = 4


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        post = get_object_or_404(Post, id=self.kwargs['pk'])

        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['total_likes'] = post.total_likes()
        context['post_is_liked'] = liked
        context['liked'] = liked
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'snippet', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostCategoryView(CreateView):
    model = Category
    template_name = 'blogapp/post_category.html'
    fields = '__all__'


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
    fields = ['title', 'category', 'snippet', 'content', 'image']

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

# The Search Functionality
def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q)

            results = Post.objects.filter(query)

    return render(request, 'blogapp/post_search.html',
                    {'form': form,
                    'q': q,
                    'results': results})


def contact(request):
	if request.method == 'POST':
		form = PostContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry"
			body = {
			'first_name': form.cleaned_data['first_name'],
			'last_name': form.cleaned_data['last_name'],
			'email': form.cleaned_data['email_address'],
			'message':form.cleaned_data['message'],
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("blogapp-home")

	form = PostContactForm()
	return render(request, "blogapp/contact.html", {'form':form})
