from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.home.forms import PostUpdateForm, PostCreateForm
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
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        post_comments = post.comments.filter(is_reply=False)
        context = {
            'post': post,
            'post_comments': post_comments,
        }
        return render(request, self.template_name, context)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        try:
            post = get_object_or_404(Post, pk=post_id)
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
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
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


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateForm
    template_name = 'home/post_create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_post = form.save(commit=False)
            new_post.user_id = request.user.id
            new_post.slug = slugify(cd['title'][:30])
            new_post.save()
            messages.success(request, 'Post created successfully', extra_tags='success')
            return redirect('home:post_detail', post_id=new_post.id, post_slug=new_post.slug)
        else:
            messages.error(request, 'Invalid Inputs', extra_tags='error')
