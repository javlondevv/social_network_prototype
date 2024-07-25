import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, CreateView, DetailView, UpdateView

from .forms import UserRegisterForm, LoginForm, PostForm, UserForm
from .models import Post, Like


def index_page_view(request):
    """
    Renders the index page if the request method is 'GET', otherwise returns a HttpResponseNotAllowed response with allowed methods.
    """
    if request.method == 'GET':
        return render(request, 'index.html', )
    else:
        return HttpResponseNotAllowed(['GET'])


class RegisterPageView(FormView):
    """
    Handles the registration page view with a form for user registration.
    Methods:
        form_valid(self, form): Processes the form data when valid, saves the data, and redirects to the success URL.
        form_invalid(self, form): Handles the case when the form data is invalid, displaying errors and rendering the registration form again.
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        print("Form is valid. Saving data.")
        print("Form:", form)
        print("Request FILES:", self.request.FILES)
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid. Errors:", form.errors)
        return render(self.request, self.template_name, {'form': form})


class LoginPageView(LoginView):
    '''
    Extends Django's LoginView to handle the login page view.
    Methods:
        get_context_data(self, **kwargs): Adds the LoginForm to the context.
        form_valid(self, form): Processes the form data when valid.
        form_invalid(self, form): Handles the case when the form data is invalid.
    '''
    form_class = LoginForm
    template_name = 'registration/login.html'
    next_page = reverse_lazy('posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = LoginForm
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """
    Extends Django's LogoutView to handle the user logout functionality with redirection to the login page.
    """
    next_page = reverse_lazy('login')


# Configure logging
logger = logging.getLogger(__name__)


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new post with login required.
    Sets the author of the post to the current user before saving.
    Logs debug information if the form is invalid.
    """
    model = Post
    form_class = PostForm
    template_name = 'add-post.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("Form is invalid. Errors: %s", form.errors)
        return super().form_invalid(form)


def BlogPostLike(request, pk):
    """
    Handles the like functionality for a blog post.

    Args:
        request: HttpRequest object containing metadata about the request.
        pk (int): The primary key of the post to be liked.

    Returns:
        HttpResponseRedirect: Redirects to the detailed view of the liked post.
    """
    post = get_object_or_404(Post, pk=pk)

    like = Like.objects.filter(user=request.user, post=post).first()

    if like:
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)
    post.update_likes_count()

    return redirect('post_detail', pk=pk)


class PostDetailView(LoginRequiredMixin, DetailView):
    """
    Handles the detailed view of a post, including checking if the current user has liked the post.

    Methods:
        post(self, request, *args, **kwargs): Redirects to the detailed view of the post.
        get_context_data(self, **kwargs): Retrieves context data including the number of likes for the post and whether the current user has liked it.
    """
    model = Post
    template_name = 'post_detail.html'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        return redirect('post_detail', pk=post.pk)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes
        data['post_is_liked'] = liked
        return data


class PostListView(ListView):
    """
    Class representing a list view of blog posts.
    Methods:
        get_queryset: Returns the queryset of posts based on filter criteria.
        get_last_liked_posts_as_notifications: Retrieves the last liked posts with details for notifications.
        get_context_data: Updates the context with pagination information and last liked posts.
    """
    template_name = 'blog_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')
        user = self.request.user

        filter_type = self.request.GET.get('filter')

        if filter_type == 'my_posts' and user.is_authenticated:
            queryset = queryset.filter(author=user)
            for post in queryset:
                print(f"Title: {post.title}, Content: {post.content.url}")
        elif filter_type == 'liked_posts' and user.is_authenticated:
            liked_post_ids = Like.objects.filter(user=user).values_list('post_id', flat=True)
            queryset = queryset.filter(id__in=liked_post_ids)
            for post in queryset:
                print(f"Title: {post.title}, Content: {post.content.url}")
        return queryset

    def get_last_liked_posts_as_notifications(self):
        user = self.request.user
        last_likes = Like.objects.filter(post__author=user).order_by('-created_at')[:5]

        if not last_likes.exists():
            return Post.objects.none(), []

        liked_posts = Post.objects.filter(id__in=last_likes.values_list('post_id', flat=True)).distinct()
        likes_with_times = [
            {
                'post': like.post,
                'liked_time': like.created_at,
                'liked_by': like.user
            }
            for like in last_likes
        ]
        return liked_posts, likes_with_times

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        pagination = context['page_obj']
        paginator = pagination.paginator
        page = pagination.number
        left = (int(page) - 4)
        if left < 1:
            left = 1
        right = (int(page) + 5)
        if right > paginator.num_pages:
            right = paginator.num_pages + 1
        context['pagination_range'] = range(left, right)
        context['filter_type'] = self.request.GET.get('filter', 'all')

        liked_posts, likes_with_times = self.get_last_liked_posts_as_notifications()
        context['liked_posts'] = liked_posts
        context['likes_with_times'] = likes_with_times

        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Handles the profile view for updating user profile information.

    Methods:
        post(self, request, *args, **kwargs): Processes the form data when submitted via POST request, displays a success message, and returns the response.
        get(self, request, **kwargs): Retrieves the user object and renders the profile update form.
        get_object(self, queryset=None): Retrieves the current user object for updating the profile.
    """
    template_name = 'registration/profile.html'
    form_class = UserForm
    success_url = reverse_lazy('profile')
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, "Your profile has been updated successfully! ✅")
        return response

    def get(self, request, **kwargs):
        self.object = self.request.user
        context = self.get_context_data(object=self.object, form=self.form_class)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        return self.request.user
