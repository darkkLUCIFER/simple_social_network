from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import reverse_lazy

from apps.account.forms import UserRegistrationForm, UserLoginForm, EditUserForm
from apps.account.models import Relation


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            email = cd['email']
            password = cd['password1']

            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, message='you registered successfully', extra_tags='alert-success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, message='You are now logged in', extra_tags='alert-success')
                if self.next:
                    return redirect(self.next)
                else:
                    return redirect('home:home')

            messages.error(request, message='Invalid credentials', extra_tags='alert-danger')

        return render(request, self.template_name, {'form': form})


class UserLogOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out', extra_tags='alert-success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        user_posts = user.posts.all()

        is_following = False
        relation = Relation.objects.filter(from_user=request.user, to_user=user).exists()
        if relation:
            is_following = True

        context = {
            'user': user,
            'user_posts': user_posts,
            'is_following': is_following,
        }
        return render(request, 'account/profile.html', context=context)


class UserPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        relation = Relation.objects.filter(from_user=request.user, to_user=self.user).exists()
        if relation:
            messages.error(request, message='You are already following', extra_tags='danger')
        else:
            Relation.objects.create(from_user=request.user, to_user=self.user)
            messages.success(request, message='You followed this user', extra_tags='alert-success')
        return redirect('account:user_profile', user_id=self.user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        relation = Relation.objects.filter(from_user=request.user, to_user=self.user)
        if relation.exists():
            relation.delete()
            messages.success(request, message='You unfollowed this user', extra_tags='alert-success')
        else:
            messages.error(request, message='You are not following this user', extra_tags='danger')

        return redirect('account:user_profile', user_id=self.user.id)


class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm
    template_name = 'account/edit_profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.profile, initial={'email': request.user.email})
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            request.user.email = cd['email']
            request.user.save()
            messages.success(request, message='Your account has been updated', extra_tags='alert-success')
        return redirect('account:user_profile', user_id=request.user.id)
