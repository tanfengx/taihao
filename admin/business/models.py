from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers

# Create your models here.
# 用户
class Member(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    name = models.CharField(max_length=255, verbose_name="姓名 ", null=True, blank=True, help_text="姓名")
    user_id = models.IntegerField(verbose_name="所属用户", null=True, blank=True, help_text="所属用户")
    username = models.CharField(max_length=255, verbose_name="用户名 ", null=True, blank=True, help_text="用户名")
    isvip = models.CharField(max_length=255, null=True, verbose_name="是否会员", help_text="是否会员", default='否')

    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "member"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

class MemberSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = '__all__'

    def get_userId(self, obj):
        return obj.user_id

# 商家
class Business(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    name = models.CharField(max_length=255, verbose_name="商家名称 ", null=True, blank=True, help_text="商家名称")
    phone = models.CharField(max_length=255, verbose_name="联系电话 ", null=True, blank=True, help_text="联系电话")
    user_id = models.IntegerField(verbose_name="所属用户", null=True, blank=True, help_text="所属用户")
    username = models.CharField(max_length=255, verbose_name="登录账号 ", null=True, blank=True, help_text="登录账号")

    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "business"
        verbose_name = "商家"
        verbose_name_plural = verbose_name

class BusinessSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = '__all__'

    def get_userId(self, obj):
        return obj.user_id


# 商品分类
class Category(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    name = models.CharField(max_length=255, verbose_name="分类名称 ", null=True, blank=True, help_text="分类名称")


    class Meta:
        db_table = "category"
        verbose_name = "商品分类"
        verbose_name_plural = verbose_name

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


# 商品
class Goods(models.Model):
    category_id = models.IntegerField(verbose_name="商品分类", null=True, blank=True, help_text="商品分类")
    content = models.TextField(verbose_name="详情 ",null=True, blank=True,  help_text="详情")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="发布时间", verbose_name="发布时间")
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    img = models.CharField(max_length=255, verbose_name="图片 ", null=True, blank=True, help_text="图片")
    name = models.CharField(max_length=255, verbose_name="商品名称 ", null=True, blank=True, help_text="商品名称")
    price = models.FloatField(verbose_name="价格 ",null=True, blank=True,  help_text="价格")
    remarks = models.CharField(max_length=255, verbose_name="审核说明 ", null=True, blank=True, help_text="审核说明")
    state_radio = models.CharField(max_length=255, verbose_name="状态,审核中|审核成功|审核失败 ", null=True, blank=True, help_text="状态,审核中|审核成功|审核失败",default="审核中")
    user_id = models.IntegerField(verbose_name="发布商家", null=True, blank=True, help_text="发布商家")
    views = models.IntegerField(verbose_name="浏览量", null=True, blank=True, help_text="浏览量")

    @property
    def categoryId(self):
        return self.category_id
    @property
    def createTime(self):
        return self.create_time
    @property
    def stateRadio(self):
        return self.state_radio
    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "goods"
        verbose_name = "商品"
        verbose_name_plural = verbose_name

class GoodsSerializer(serializers.ModelSerializer):
    categoryId = serializers.SerializerMethodField()
    createTime = serializers.SerializerMethodField()
    stateRadio = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = '__all__'

    def get_categoryId(self, obj):
        return obj.category_id
    def get_createTime(self, obj):
        return obj.create_time
    def get_stateRadio(self, obj):
        return obj.state_radio
    def get_userId(self, obj):
        return obj.user_id

# 购物车
class Cart(models.Model):
    biz_user_id = models.IntegerField(verbose_name="商家", null=True, blank=True, help_text="商家")
    goodid = models.IntegerField(verbose_name="产品编号", null=True, blank=True, help_text="产品编号")
    id = models.AutoField(primary_key=True, verbose_name="购物车编号", help_text="购物车编号")
    img = models.CharField(max_length=255, verbose_name="商品图片 ", null=True, blank=True, help_text="商品图片")
    name = models.CharField(max_length=255, verbose_name="购买商品 ", null=True, blank=True, help_text="购买商品")
    num = models.IntegerField(verbose_name="数量", null=True, blank=True, help_text="数量")
    price = models.FloatField(verbose_name="单价 ",null=True, blank=True,  help_text="单价")
    user_id = models.IntegerField(verbose_name="购买用户", null=True, blank=True, help_text="购买用户")

    @property
    def bizUserId(self):
        return self.biz_user_id
    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "cart"
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

class CartSerializer(serializers.ModelSerializer):
    bizUserId = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_bizUserId(self, obj):
        return obj.biz_user_id
    def get_userId(self, obj):
        return obj.user_id

# 订单评论
class Comments(models.Model):
    biz_user_id = models.IntegerField(verbose_name="商家编号", null=True, blank=True, help_text="商家编号")
    content = models.TextField(verbose_name="评论内容 ",null=True, blank=True,  help_text="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="添加时间", verbose_name="添加时间")
    goods_id = models.IntegerField(verbose_name="商品编号", null=True, blank=True, help_text="商品编号")
    id = models.AutoField(primary_key=True, verbose_name="评论编号", help_text="评论编号")
    orders_id = models.IntegerField(verbose_name="订单编号", null=True, blank=True, help_text="订单编号")
    pid = models.IntegerField(verbose_name="父评论ID", null=True, blank=True, help_text="父评论ID")
    puser_id = models.IntegerField(verbose_name="父级用户ID", null=True, blank=True, help_text="父级用户ID")
    score = models.IntegerField(verbose_name="评论星级", null=True, blank=True, help_text="评论星级")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",verbose_name="修改时间")
    user_id = models.IntegerField(verbose_name="用户", null=True, blank=True, help_text="用户")

    @property
    def bizUserId(self):
        return self.biz_user_id
    @property
    def createTime(self):
        return self.create_time
    @property
    def goodsId(self):
        return self.goods_id
    @property
    def ordersId(self):
        return self.orders_id
    @property
    def puserId(self):
        return self.puser_id
    @property
    def updateTime(self):
        return self.update_time
    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "comments"
        verbose_name = "订单评论"
        verbose_name_plural = verbose_name

class CommentsSerializer(serializers.ModelSerializer):
    bizUserId = serializers.SerializerMethodField()
    createTime = serializers.SerializerMethodField()
    goodsId = serializers.SerializerMethodField()
    ordersId = serializers.SerializerMethodField()
    puserId = serializers.SerializerMethodField()
    updateTime = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = '__all__'

    def get_bizUserId(self, obj):
        return obj.biz_user_id
    def get_createTime(self, obj):
        return obj.create_time
    def get_goodsId(self, obj):
        return obj.goods_id
    def get_ordersId(self, obj):
        return obj.orders_id
    def get_puserId(self, obj):
        return obj.puser_id
    def get_updateTime(self, obj):
        return obj.update_time
    def get_userId(self, obj):
        return obj.user_id

# 自行车订单
class Orders(models.Model):
    amount = models.FloatField(verbose_name="总金额 ",null=True, blank=True,  help_text="总金额")
    biz_user_id = models.IntegerField(verbose_name="商户", null=True, blank=True, help_text="商户")
    content = models.TextField(verbose_name="订单明细 ",null=True, blank=True,  help_text="订单明细")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="下单时间", verbose_name="下单时间")
    goodids = models.CharField(max_length=255, verbose_name="产品编号 ", null=True, blank=True, help_text="产品编号")
    id = models.AutoField(primary_key=True, verbose_name="订单编号", help_text="订单编号")
    name = models.CharField(max_length=255, verbose_name="订单号 ", null=True, blank=True, help_text="订单号")
    state_radio = models.CharField(max_length=255, verbose_name="订单状态,已下单|已发货|已收货|已评价|已取消 ", null=True, blank=True, help_text="订单状态,已下单|已发货|已收货|已评价|已取消")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="更新时间",verbose_name="更新时间")
    user_id = models.IntegerField(verbose_name="下单用户", null=True, blank=True, help_text="下单用户")

    @property
    def bizUserId(self):
        return self.biz_user_id
    @property
    def createTime(self):
        return self.create_time
    @property
    def stateRadio(self):
        return self.state_radio
    @property
    def updateTime(self):
        return self.update_time
    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "orders"
        verbose_name = "自行车订单"
        verbose_name_plural = verbose_name

class OrdersSerializer(serializers.ModelSerializer):
    bizUserId = serializers.SerializerMethodField()
    createTime = serializers.SerializerMethodField()
    stateRadio = serializers.SerializerMethodField()
    updateTime = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = '__all__'

    def get_bizUserId(self, obj):
        return obj.biz_user_id
    def get_createTime(self, obj):
        return obj.create_time
    def get_stateRadio(self, obj):
        return obj.state_radio
    def get_updateTime(self, obj):
        return obj.update_time
    def get_userId(self, obj):
        return obj.user_id

# 支付方式
class Paytype(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="方式编号", help_text="方式编号")
    img = models.CharField(max_length=255, verbose_name="二维码 ", null=True, blank=True, help_text="二维码")
    name = models.CharField(max_length=255, verbose_name="支付名称 ", null=True, blank=True, help_text="支付名称")


    class Meta:
        db_table = "paytype"
        verbose_name = "支付方式"
        verbose_name_plural = verbose_name

class PaytypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paytype
        fields = '__all__'


# 收货地址
class Address(models.Model):
    address = models.CharField(max_length=255, verbose_name="详细地址 ", null=True, blank=True, help_text="详细地址")
    default_radio = models.CharField(max_length=255, verbose_name="是否默认 ", null=True, blank=True, help_text="是否默认")
    id = models.AutoField(primary_key=True, verbose_name="收货地址编号", help_text="收货地址编号")
    name = models.CharField(max_length=255, verbose_name="姓名 ", null=True, blank=True, help_text="姓名")
    phone = models.CharField(max_length=255, verbose_name="手机 ", null=True, blank=True, help_text="手机")
    postcode = models.CharField(max_length=255, verbose_name="邮编 ", null=True, blank=True, help_text="邮编")
    user_id = models.IntegerField(verbose_name="用户编号", null=True, blank=True, help_text="用户编号")

    @property
    def defaultRadio(self):
        return self.default_radio
    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "address"
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

class AddressSerializer(serializers.ModelSerializer):
    defaultRadio = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = '__all__'

    def get_defaultRadio(self, obj):
        return obj.default_radio
    def get_userId(self, obj):
        return obj.user_id

# 自行车收藏
class Collect(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")
    goods_id = models.IntegerField(verbose_name="商品", null=True, blank=True, help_text="商品")
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="更新时间",verbose_name="更新时间")
    user_id = models.IntegerField(verbose_name="用户", null=True, blank=True, help_text="用户")

    @property
    def createTime(self):
        return self.create_time
    @property
    def goodsId(self):
        return self.goods_id
    @property
    def updateTime(self):
        return self.update_time
    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "collect"
        verbose_name = "自行车收藏"
        verbose_name_plural = verbose_name

class CollectSerializer(serializers.ModelSerializer):
    createTime = serializers.SerializerMethodField()
    goodsId = serializers.SerializerMethodField()
    updateTime = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Collect
        fields = '__all__'

    def get_createTime(self, obj):
        return obj.create_time
    def get_goodsId(self, obj):
        return obj.goods_id
    def get_updateTime(self, obj):
        return obj.update_time
    def get_userId(self, obj):
        return obj.user_id

# 售后服务
class Services(models.Model):
    content = models.TextField(verbose_name="具体原因 ",null=True, blank=True,  help_text="具体原因")
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    orders_id = models.IntegerField(verbose_name="售后订单", null=True, blank=True, help_text="售后订单")
    remarks = models.CharField(max_length=255, verbose_name="处理说明 ", null=True, blank=True, help_text="处理说明")
    state_radio = models.CharField(max_length=255, verbose_name="状态,审核中|审核通过|审核失败|处理完成 ", null=True, blank=True, help_text="状态,审核中|审核通过|审核失败|处理完成",default='审核中')
    type_radio = models.CharField(max_length=255, verbose_name="类型,退货|换货|退款 ", null=True, blank=True, help_text="类型,退货|换货|退款")
    user_id = models.IntegerField(verbose_name="用户", null=True, blank=True, help_text="用户")

    @property
    def ordersId(self):
        return self.orders_id
    @property
    def stateRadio(self):
        return self.state_radio
    @property
    def typeRadio(self):
        return self.type_radio
    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "services"
        verbose_name = "售后服务"
        verbose_name_plural = verbose_name

class ServicesSerializer(serializers.ModelSerializer):
    ordersId = serializers.SerializerMethodField()
    stateRadio = serializers.SerializerMethodField()
    typeRadio = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Services
        fields = '__all__'

    def get_ordersId(self, obj):
        return obj.orders_id
    def get_stateRadio(self, obj):
        return obj.state_radio
    def get_typeRadio(self, obj):
        return obj.type_radio
    def get_userId(self, obj):
        return obj.user_id


# 轮播图
class Banner(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="轮播图编号", help_text="轮播图编号")
    img = models.CharField(max_length=255, verbose_name="图片 ", null=True, blank=True, help_text="图片")
    index_radio = models.CharField(max_length=255, verbose_name="是否首页 ", null=True, blank=True, help_text="是否首页")
    url = models.CharField(max_length=255, verbose_name="链接地址 ", null=True, blank=True, help_text="链接地址")

    @property
    def indexRadio(self):
        return self.index_radio

    class Meta:
        db_table = "banner"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

class BannerSerializer(serializers.ModelSerializer):
    indexRadio = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = '__all__'

    def get_indexRadio(self, obj):
        return obj.index_radio

