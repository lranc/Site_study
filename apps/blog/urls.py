from django.urls import path
from . import views

app_name = 'blog'
# start with blog
urlpatterns = [
    # http://localhost:8000/blog/
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('<int:blog_pk>', views.BlogDetailView.as_view(), name="blog_detail"),
    path('type/<int:blog_type_pk>', views.BlogTypeListView.as_view(), name="blogs_with_type"),
    path('date/<int:year>/<int:month>', views.BlogDateListView.as_view(), name="blogs_with_date"),
    # path('newblog/',views.NewBlogView.as_view(),name='new_blog'),
    # path('updateblog/<int:pk>',views.UpdateBlogView.as_view(),name='update_blog'),
]