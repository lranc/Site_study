import time
import re
from rest_framework import viewsets, serializers
from novels.models import Novel
from novels.serializers import NovelSerializer
from trades.models import ShoppingCart, OrderGoods, OrderInfo
from random import Random
from lranc_site.settings import REGEX_MOBILE


class ShopCartSerializer(serializers.Serializer):
    # 使用Serializer, 灵活性高, 需要重复添加时更新数量
    # 而modelSerialzer会在create的时候进行is_valid验证, 导致无法重复添加
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "数量不能小于一",
                                        "required": "请选择购买数量"
                                    })
    novel = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Novel.objects.all())

    # 继承的Serializer没有save功能，必须写一个create方法
    def create(self, validated_data):
        # 获取当前用户
        # validated_data是已经处理过的数据
        # view中:self.request.user; serizlizer中:self.context["request"].user
        user = self.context["request"].user
        nums = validated_data["nums"]
        novel = validated_data["novel"]
        # 如果购物车该作品已存在则 + nums值, 否则创建
        existed = ShoppingCart.objects.filter(user=user, novel=novel)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            # 添加到购物车
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class ShopCartDetailSerializer(serializers.ModelSerializer):
    '''
    购物车商品详情信息
    '''
    # 一个购物车对应一个商品
    novel = NovelSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("novel", "nums")


class OrderGoodsSerialzier(serializers.ModelSerializer):
    # 订单中的商品
    novel = NovelSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    # 订单商品信息
    goods = OrderGoodsSerialzier(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    # 当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 生成订单的时候这些不用post, read_only
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    nonce_str = serializers.CharField(read_only=True)
    pay_type = serializers.CharField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)

    # 验证手机号码(函数名称必须为 validate_ + 该字段名)
    def validate_singer_mobile(self, singer_mobile):
        """
        手机号码验证
        """
        if not re.match(REGEX_MOBILE, singer_mobile):
            raise serializers.ValidationError("请输入正确的手机号码")
        return singer_mobile

    # 支付订单的url
    # alipay_url = serializers.SerializerMethodField(read_only=True)

    # def get_alipay_url(self, obj):
    #     alipay = AliPay(
    #         appid="2016091500517456",
    #         app_notify_url="http://47.93.198.159:8000/alipay/return/",
    #         app_private_key_path=private_key_path,
    #         alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    #         debug=True,  # 默认False,
    #         return_url="http://47.93.198.159:8000/alipay/return/"
    #     )

    #     url = alipay.direct_pay(
    #         subject=obj.order_sn,
    #         out_trade_no=obj.order_sn,
    #         total_amount=obj.order_mount,
    #     )
    #     re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

    #     return re_url

    def generate_order_sn(self):
        # 生成订单号
        # 当前时间+userid+随机数
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        # validate中添加order_sn，然后在view中就可以save
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
