from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages

from apps.account.forms import UserRegistrationForm


class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            email = cd['email']
            password1 = cd['password']

            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, message='you registered successfully', extra_tags='alert-success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})
