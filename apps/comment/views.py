from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.comment.forms import CreateCommentForm
from apps.comment.models import Comment
from apps.home.models import Post


class ReplyCommentView(LoginRequiredMixin, View):
    form_class = CreateCommentForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply submitted successfully', extra_tags='success')
        return redirect('home:post_detail', post_id=post.id, post_slug=post.slug)
