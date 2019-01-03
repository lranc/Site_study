from django.urls import path
from . import views

app_name = 'operation'
urlpatterns = [
    path('like_change', views.LikeView.as_view(), name='like_change'),
    path('add_comment', views.AddComment.as_view(), name='add_comment')
]