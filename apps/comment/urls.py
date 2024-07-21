from django.urls import path
from apps.comment import views

app_name = 'comment'

urlpatterns = [
    path('reply/<int:post_id>/<int:comment_id>/', views.ReplyCommentView.as_view(), name='reply_comment'),
]
