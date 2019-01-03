from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Blog, BlogType
from utils.page_data import get_page_data
from django.views.generic import ListView
from pure_pagination.mixins import PaginationMixin
from read_statistic.utils import read_statistic_once_read
# Create your views here.


class BlogListView(View):
    # blog首页
    def get(self, request):
        blogs_all_list = Blog.objects.all()
        datas = get_page_data(request, blogs_all_list, 10)
        context = {}
        context['datas'] = datas
        return render(request, 'blog/blog_list.html', context)

# 暂时还不够熟练
# class BlogListView(PaginationMixin, ListView):
#     paginate_by = 1
#     model = Blog
#     template_name = "blog/blog_list.html"
#     queryset = Blog.objects.all()


class BlogTypeListView(View):
    # 返回某一类型的博客
    def get(self, request, blog_type_pk):
        context = {}
        blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
        blog_type_list = Blog.objects.filter(
            blog_type=blog_type_pk).order_by('-created_time')

        context['datas'] = get_page_data(request, blog_type_list, 10)
        context['blog_type'] = blog_type
        return render(request, 'blog/blog_list.html', context)


class BlogDateListView(View):
    def get(self, request, year, month):
        context = {}
        blog_date_list = Blog.objects.filter(
            created_time__year=year, created_time__month=month)
        context['datas'] = get_page_data(request, blog_date_list, 10)
        context['datestr'] = '{}年{}月'.format(year, month)
        return render(request, 'blog/blog_list.html', context)


class BlogDetailView(View):
    def get(self, request, blog_pk):
        blog = get_object_or_404(Blog, pk=blog_pk)
        read_cookie_key = read_statistic_once_read(request, blog)

        context = {}
        context['previous_blog'] = Blog.objects.filter(
            created_time__lt=blog.created_time).first()
        context['next_blog'] = Blog.objects.filter(
            created_time__gt=blog.created_time).last()
        context['blog'] = blog
        response = render(request, 'blog/blog_detail.html', context)  # 响应
        response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
        return response
