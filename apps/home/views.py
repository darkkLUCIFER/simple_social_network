from django.shortcuts import render
from django.views import View

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
