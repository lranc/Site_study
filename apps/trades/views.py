# -*- coding:utf8 -*-

from trades.models import ShoppingCart, OrderInfo, OrderGoods
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from trades.serializers import ShopCartSerializer, ShopCartDetailSerializer,\
    OrderSerializer, OrderDetailSerializer


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        删除购物记录
    update:
        修改记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication)

    # 以作品的id查询, lookup_field用于查询的字段, 默认为shopcart的id
    lookup_field = "novel_id"

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    # 获取购物车列表
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewset(
        mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    """
    # 不允许update 因此不使用modelviewset
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication)
    # 动态配置serializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    # 获取订单列表
    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    # 在订单提交保存之前还需要多两步步骤，所以这里自定义perform_create方法
    # 1.将购物车中的商品保存到OrderGoods中
    # 2.清空购物车
    def perform_create(self, serializer):
        order = serializer.save()
        # 获取购物车所有商品
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.novel = shop_cart.novel
            order_goods.novel_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            # 清空购物车
            shop_cart.delete()
        return order

    def create(self, request, *args, **kwargs):
        shop_carts_num = ShoppingCart.objects.filter(
            user=self.request.user).count()
        if not shop_carts_num:
            return Response({"shop_carts": '购物车内无商品'
                             }, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.perform_create(serializer)
        response_dict = serializer.data
        headers = self.get_success_headers(serializer.data)
        return Response(response_dict, status=status.HTTP_201_CREATED, headers=headers)