from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from accounts.forms import LoginForm, CustomUserCreationForm, UserChangeForm
from posts.models import Post


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            messages.error(request, "Некорректные данные")
            return redirect('index_page')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.warning(request, "Пользователь не найден")
            return redirect('index_page')
        login(request, user)
        messages.success(request, 'Добро пожаловать')
        next = request.GET.get('next')
        if next:
            return redirect(next)
        return redirect('main')


def logout_view(request):
    logout(request)
    return redirect('index_page')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        return self.form_invalid(form)

    def form_valid(self, form, request):
        response = super().form_valid(form)
        user = form.save()
        login(request, user)
        return response

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return UserChangeForm(**form_kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['subscriber_count'] = user.subscribers.count()
        context['subscription_count'] = user.subscriptions.count()
        context['post_count'] = user.posts.count()
        return context


class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


def like_post(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    user = request.user
    if user in post.user_likes.all():
        post.likes_count -= 1
        post.user_likes.remove(user)
        post.save()
        messages.success(request, 'Post unliked successfully.')
    else:
        post.likes_count += 1
        post.user_likes.add(user)
        post.save()
        messages.success(request, 'Post liked successfully.')
    return redirect('main')
