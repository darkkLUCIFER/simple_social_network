from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.home.models import Post


class HomeView(View):
    template_name = 'home/index.html'

    def get(self, request):
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, self.template_name, context)


class PostDetailView(View):
    template_name = 'home/post_detail.html'

    def get(self, request, post_id, post_slug):
        try:
            post = Post.objects.get(pk=post_id, slug=post_slug)
        except Post.DoesNotExist:
            post = None
        context = {
            'post': post
        }
        return render(request, self.template_name, context)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            if post.user.id == request.user.id:
                post.delete()
                messages.success(request, 'Post deleted successfully', extra_tags='success')
            else:
                messages.error(request, 'You are not authorized to delete this post', extra_tags='error')
        except Post.DoesNotExist:
            messages.warning(request, 'Post does not exist', extra_tags='warning')
        return redirect('home:home')
