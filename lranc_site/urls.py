# -*- coding:utf8 -*-

import xadmin
from django.urls import path, include, re_path
from django.views.static import serve
from lranc_site.settings import MEDIA_ROOT
from django.views.generic import RedirectView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from authors.views import NovelAuthorsViewSet, AuthorReaderViewSet
from novels.views import NovelTagsViewSet, NovelViewSet
from users.views import SmsCodeViewset, UserViewset
from operation.views import UserFavNovelsViewset, CommentViewset, VerifycodeViewSet, VerifycodeAPIView
from trades.views import ShoppingCartViewset, OrderViewset
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token


# from lranc_site.hrbridrouter import HybridRouter
# APIView注册
# router = HybridRouter()
# router.register('imagecode', VerifycodeViewSet, base_name="imagecode")
# router.register('authors', NovelAuthorsViewSet, base_name='authors')
# router.add_api_view('imageapi', path('imageapi/<int:image_code_id>',VerifycodeAPIView,name='imageapi'))
router = DefaultRouter()
# 图片验证码
router.register('imagecode', VerifycodeViewSet, base_name="imagecode")
# 配置authors的url
router.register('authors', NovelAuthorsViewSet, base_name='authors')
router.register('rankreaders', AuthorReaderViewSet, base_name='rankreaders')
router.register('noveltags', NovelTagsViewSet, base_name='rankreaders')
router.register('novels', NovelViewSet, base_name='novels')
# 验证码VerifyCode的url
router.register('verifycode', SmsCodeViewset, base_name="verifycode")
# 用户url
router.register('users', UserViewset, base_name="users")
# 用户收藏作品url
router.register('favnovels', UserFavNovelsViewset, base_name="favnovels")
# 用户评论
router.register('usercomment', CommentViewset, base_name="usercomment")
# 购物车url
router.register('shopcarts', ShoppingCartViewset, base_name="shopcarts")
# 订单url
router.register('orders', OrderViewset, base_name="orders")


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('docs/', include_docs_urls(title='lranc文档')),
    path('api-auth/', include('rest_framework.urls')),
    re_path('^', include(router.urls), name='Lranc'),
    # drf自带的token授权登录,获取token需要向该地址post数据
    path('api-token-auth/', views.obtain_auth_token),
    # jwt 认证
    path('login/', obtain_jwt_token),
    # 配置上传文件的访问处理函数, 处理图片显示的url
    # 使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)',  serve, {"document_root": MEDIA_ROOT}),
    # 验证码url
    path("captcha/", include('captcha.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
    # 配置ckeditor路由
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('verifycodes/<int:image_code_id>', VerifycodeView.as_view())
]
