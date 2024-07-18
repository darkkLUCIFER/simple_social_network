from django.shortcuts import render
from django.views import View

from apps.home.models import Post


class HomeView(View):
    template_name = 'home/index.html'

    def get(self, request):
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, self.template_name, context)
