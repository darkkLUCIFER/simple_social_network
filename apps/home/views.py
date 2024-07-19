from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.home.forms import PostUpdateForm
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


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    template_name = 'home/post_update.html'

    def setup(self, request, *args, **kwargs):
        try:
            self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        except Post.DoesNotExist:
            self.post_instance = None
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.post_instance:
            if not self.post_instance.user.id == request.user.id:
                messages.error(request, 'You are not authorized to edit this post', extra_tags='error')
                return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.post_instance)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if self.post_instance:
            form = self.form_class(request.POST, instance=self.post_instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post updated successfully', extra_tags='success')
                return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)
        else:
            messages.error(request, 'post does not exist', extra_tags='error')
