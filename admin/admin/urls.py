"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve

from admin import settings
from business.views.front import *
from system.base.dict import *
from system.base.file import *
from system.base.login import *
from system.base.notice import *
from system.base.permission import *
from system.base.register import *
from system.base.role import *
from system.base.user import *
from business.views.member import *
from business.views.business import *
from business.views.category import *
from business.views.goods import *
from business.views.cart import *
from business.views.comments import *
from business.views.orders import *
from business.views.paytype import *
from business.views.address import *
from business.views.collect import *
from business.views.services import *
from business.views.banner import *
from business.views.front import *


urlpatterns = [
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('logout/<str:id>', LogoutView.as_view()),
    path('user', UserView.as_view(),name="user"),
    path('user/<int:pk>', UserView.as_view(), name='user_detail'),
    path('user/page', UserPageView.as_view(), name="user_page"),
    path('user/del/batch', UserBatchDeleteAPIView.as_view(),name="user_batch_delete"),
    path('user/export', UserExport.as_view(),name="user_export"),
    path('updateUser', UserInfoUpdate.as_view(),name="user_info_update"),
    path('password/change', UserUpdatePwd.as_view(),name="user_update_pwd"),
    path('role', RoleView.as_view(),name="role"),
    path('role/<int:pk>', RoleView.as_view(), name='role_detail'),
    path('role/page', RolePageView.as_view(), name="role_page"),
    path('role/del/batch', RoleBatchDeleteAPIView.as_view(), name="role_batch_delete"),
    path('role/export', RoleExport.as_view(),name="role_export"),
    path('permission', PermissionView.as_view(),name="permission"),
    path('permission/<int:pk>', PermissionView.as_view(), name='permission_delete'),
    path('permission/del/batch', PermissionBatchDeleteAPIView.as_view(), name="permission_batch_delete"),
    path('permission/export', PermissionExport.as_view(),name="permission_export"),
    path('dict', DictView.as_view(), name="dict"),
    path('dict/<int:pk>', DictView.as_view(), name='dict_detail'),
    path('dict/page', DictPageView.as_view(), name="dict_page"),
    path('dict/del/batch', DictBatchDeleteAPIView.as_view(), name="dict_batch_delete"),
    path('dict/export', DictExport.as_view(),name="dict_export"),
    path('file/upload', FileUploadView.as_view(),name="file_upload"),
    path('file/uploadImg', FileUploadEditorView.as_view(),name="file_upload_editor"),
    path('notice', NoticeView.as_view(), name="notice"),
    path('notice/<int:pk>', NoticeView.as_view(), name='notice_detail'),
    path('notice/page', NoticePageView.as_view(), name="notice_page"),
    path('notice/del/batch', NoticeBatchDeleteAPIView.as_view(), name="notice_batch_delete"),
    path('notice/export', NoticeExport.as_view(), name="notice_export"),

    # 用户
    path('member', MemberView.as_view(), name="member"),
    path('member/<int:pk>', MemberView.as_view(), name='member_detail'),
    path('member/page', MemberPageView.as_view(), name="member_page"),
    path('member/del/batch', MemberBatchDeleteAPIView.as_view(), name="member_batch_delete"),
    path('member/export', MemberExport.as_view(), name="member_export"),
    path('front/member/user/<int:userId>', getMemberByUserId.as_view(), name="getMemberByUserId"),
    path('front/member/update', UpdateMember.as_view(), name="UpdateMember"),
    # 商家
    path('business', BusinessView.as_view(), name="business"),
    path('business/<int:pk>', BusinessView.as_view(), name='business_detail'),
    path('business/page', BusinessPageView.as_view(), name="business_page"),
    path('business/del/batch', BusinessBatchDeleteAPIView.as_view(), name="business_batch_delete"),
    path('business/export', BusinessExport.as_view(), name="business_export"),
    path('front/business/user/<int:userId>', getBusinessByUserId.as_view(), name="getBusinessByUserId"),
    path('front/business/update', UpdateBusiness.as_view(), name="UpdateBusiness"),

    # 商品分类
    path('category', CategoryView.as_view(), name="category"),
    path('category/<int:pk>', CategoryView.as_view(), name='category_detail'),
    path('category/page', CategoryPageView.as_view(), name="category_page"),
    path('category/del/batch', CategoryBatchDeleteAPIView.as_view(), name="category_batch_delete"),
    path('category/export', CategoryExport.as_view(), name="category_export"),
    path('front/category/update', UpdateCategory.as_view(), name="UpdateCategory"),
    # 商品
    path('goods', GoodsView.as_view(), name="goods"),
    path('goods/<int:pk>', GoodsView.as_view(), name='goods_detail'),
    path('goods/page', GoodsPageView.as_view(), name="goods_page"),
    path('goods/del/batch', GoodsBatchDeleteAPIView.as_view(), name="goods_batch_delete"),
    path('goods/export', GoodsExport.as_view(), name="goods_export"),
    path('front/goods/update', UpdateGoods.as_view(), name="UpdateGoods"),
    # 购物车
    path('cart', CartView.as_view(), name="cart"),
    path('cart/<int:pk>', CartView.as_view(), name='cart_detail'),
    path('cart/page', CartPageView.as_view(), name="cart_page"),
    path('cart/del/batch', CartBatchDeleteAPIView.as_view(), name="cart_batch_delete"),
    path('cart/export', CartExport.as_view(), name="cart_export"),
    path('front/cart/update', UpdateCart.as_view(), name="UpdateCart"),
    # 订单评论
    path('comments', CommentsView.as_view(), name="comments"),
    path('comments/<int:pk>', CommentsView.as_view(), name='comments_detail'),
    path('comments/page', CommentsPageView.as_view(), name="comments_page"),
    path('comments/del/batch', CommentsBatchDeleteAPIView.as_view(), name="comments_batch_delete"),
    path('comments/export', CommentsExport.as_view(), name="comments_export"),
    path('front/comments/update', UpdateComments.as_view(), name="UpdateComments"),
    # 自行车订单
    path('orders', OrdersView.as_view(), name="orders"),
    path('orders/<int:pk>', OrdersView.as_view(), name='orders_detail'),
    path('orders/page', OrdersPageView.as_view(), name="orders_page"),
    path('orders/del/batch', OrdersBatchDeleteAPIView.as_view(), name="orders_batch_delete"),
    path('orders/export', OrdersExport.as_view(), name="orders_export"),
    path('front/orders/update', UpdateOrders.as_view(), name="UpdateOrders"),
    # 支付方式
    path('paytype', PaytypeView.as_view(), name="paytype"),
    path('paytype/<int:pk>', PaytypeView.as_view(), name='paytype_detail'),
    path('paytype/page', PaytypePageView.as_view(), name="paytype_page"),
    path('paytype/del/batch', PaytypeBatchDeleteAPIView.as_view(), name="paytype_batch_delete"),
    path('paytype/export', PaytypeExport.as_view(), name="paytype_export"),
    path('front/paytype/update', UpdatePaytype.as_view(), name="UpdatePaytype"),
    # 收货地址
    path('address', AddressView.as_view(), name="address"),
    path('address/<int:pk>', AddressView.as_view(), name='address_detail'),
    path('address/page', AddressPageView.as_view(), name="address_page"),
    path('address/del/batch', AddressBatchDeleteAPIView.as_view(), name="address_batch_delete"),
    path('address/export', AddressExport.as_view(), name="address_export"),
    path('front/address/update', UpdateAddress.as_view(), name="UpdateAddress"),
    # 自行车收藏
    path('collect', CollectView.as_view(), name="collect"),
    path('collect/<int:pk>', CollectView.as_view(), name='collect_detail'),
    path('collect/page', CollectPageView.as_view(), name="collect_page"),
    path('collect/del/batch', CollectBatchDeleteAPIView.as_view(), name="collect_batch_delete"),
    path('collect/export', CollectExport.as_view(), name="collect_export"),
    path('front/collect/update', UpdateCollect.as_view(), name="UpdateCollect"),
    # 售后服务
    path('services', ServicesView.as_view(), name="services"),
    path('services/<int:pk>', ServicesView.as_view(), name='services_detail'),
    path('services/page', ServicesPageView.as_view(), name="services_page"),
    path('services/del/batch', ServicesBatchDeleteAPIView.as_view(), name="services_batch_delete"),
    path('services/export', ServicesExport.as_view(), name="services_export"),
    path('front/services/update', UpdateServices.as_view(), name="UpdateServices"),
	
    # 轮播图
    path('banner', BannerView.as_view(), name="banner"),
    path('banner/<int:pk>', BannerView.as_view(), name='banner_detail'),
    path('banner/page', BannerPageView.as_view(), name="banner_page"),
    path('banner/del/batch', BannerBatchDeleteAPIView.as_view(), name="banner_batch_delete"),
    path('banner/export', BannerExport.as_view(), name="banner_export"),

    # 前台-用户
    path('front/user/list', UserListDetail.as_view(), name="front_user_list"),
    path('front/user/<int:pk>', UserListDetail.as_view(), name='front_user_detail'),
    path('front/user/page', UserPage.as_view(), name="front_user_page"),
    # 前台-网站公告
    path('front/notice/list', NoticeListDetail.as_view(), name="front_notice_list"),
    path('front/notice/<int:pk>', NoticeListDetail.as_view(), name='front_notice_detail'),
    path('front/notice/page', NoticePage.as_view(), name="front_notice_page"),
    # 前台-轮播图
    path('front/banner/list', BannerListDetail.as_view(), name="front_banner_list"),
    path('front/banner', BannerListDetail.as_view(), name="front_banner"),
    path('front/banner/<int:pk>', BannerListDetail.as_view(), name='front_banner_detail'),
    path('front/banner/page', BannerPage.as_view(), name='front_banner_page'),
    # 前台-用户
    path('front/member/list', MemberListDetail.as_view(), name="front_member_list"),
    path('front/member', MemberListDetail.as_view(), name="front_member"),
    path('front/member/<int:pk>', MemberListDetail.as_view(), name='front_member_detail'),
    path('front/member/page', MemberPage.as_view(), name='front_member_page'),
    # 前台-商家
    path('front/business/list', BusinessListDetail.as_view(), name="front_business_list"),
    path('front/business', BusinessListDetail.as_view(), name="front_business"),
    path('front/business/<int:pk>', BusinessListDetail.as_view(), name='front_business_detail'),
    path('front/business/page', BusinessPage.as_view(), name='front_business_page'),
    # 前台-商品分类
    path('front/category/list', CategoryListDetail.as_view(), name="front_category_list"),
    path('front/category', CategoryListDetail.as_view(), name="front_category"),
    path('front/category/<int:pk>', CategoryListDetail.as_view(), name='front_category_detail'),
    path('front/category/page', CategoryPage.as_view(), name='front_category_page'),
    # 前台-浏览自行车
    path('front/goods/list', GoodsListDetail.as_view(), name="front_goods_list"),
    path('front/goods', GoodsListDetail.as_view(), name="front_goods"),
    path('front/goods/<int:pk>', GoodsListDetail.as_view(), name='front_goods_detail'),
    path('front/goods/page', GoodsPage.as_view(), name='front_goods_page'),
    path('front/goods/recom', GoodsListRecom.as_view(), name="front_goods_recom"),
    # 前台-购物车
    path('front/cart/list', CartListDetail.as_view(), name="front_cart_list"),
    path('front/cart', CartListDetail.as_view(), name="front_cart"),
    path('front/cart/<int:pk>', CartListDetail.as_view(), name='front_cart_detail'),
    path('front/cart/page', CartPage.as_view(), name='front_cart_page'),
    # 前台-订单评论
    path('front/comments/list', CommentsListDetail.as_view(), name="front_comments_list"),
    path('front/comments', CommentsListDetail.as_view(), name="front_comments"),
    path('front/comments/<int:pk>', CommentsListDetail.as_view(), name='front_comments_detail'),
    path('front/comments/page', CommentsPage.as_view(), name='front_comments_page'),
    # 前台-商品订单
    path('front/orders/list', OrdersListDetail.as_view(), name="front_orders_list"),
    path('front/orders', OrdersListDetail.as_view(), name="front_orders"),
    path('front/orders/<int:pk>', OrdersListDetail.as_view(), name='front_orders_detail'),
    path('front/orders/page', OrdersPage.as_view(), name='front_orders_page'),
    # 前台-支付方式
    path('front/paytype/list', PaytypeListDetail.as_view(), name="front_paytype_list"),
    path('front/paytype', PaytypeListDetail.as_view(), name="front_paytype"),
    path('front/paytype/<int:pk>', PaytypeListDetail.as_view(), name='front_paytype_detail'),
    path('front/paytype/page', PaytypePage.as_view(), name='front_paytype_page'),
    # 前台-收货地址
    path('front/address/list', AddressListDetail.as_view(), name="front_address_list"),
    path('front/address', AddressListDetail.as_view(), name="front_address"),
    path('front/address/<int:pk>', AddressListDetail.as_view(), name='front_address_detail'),
    path('front/address/page', AddressPage.as_view(), name='front_address_page'),
    # 前台-自行车收藏
    path('front/collect/list', CollectListDetail.as_view(), name="front_collect_list"),
    path('front/collect', CollectListDetail.as_view(), name="front_collect"),
    path('front/collect/<int:pk>', CollectListDetail.as_view(), name='front_collect_detail'),
    path('front/collect/page', CollectPage.as_view(), name='front_collect_page'),
    # 前台-售后服务
    path('front/services/list', ServicesListDetail.as_view(), name="front_services_list"),
    path('front/services', ServicesListDetail.as_view(), name="front_services"),
    path('front/services/<int:pk>', ServicesListDetail.as_view(), name='front_services_detail'),
    path('front/services/page', ServicesPage.as_view(), name='front_services_page'),
    path('front/services/mypage', MyServicesPage.as_view(), name='front_my_services_page'),
    #修改购物车
    path('front/cart/update', UpdateCart.as_view(), name="front_updateCart"),

    #修改收货地址
    path('front/address/update', UpdateAddress.as_view(), name="front_updateaddress"),
    #设置默认收货地址
    path('front/address/setDefault/<int:pk>', UpdateAddressDefault.as_view(), name="front_updateaddress_default"),

    #添加/修改订单
    path('front/orders/update', UpdateOrders.as_view(), name="front_updateOrders"),
    #取消订单
    path('front/orders/cancel/<int:pk>', CancelOrders.as_view(), name="front_cancelOrders"),

    #查看订单评价
    path('front/comments/tree', CommentsTree.as_view(), name="front_comments_tree"),
    #添加/修改订单评价
    path('front/comments/update', UpdateComments.as_view(), name="front_updatecomments"),

    #统计-商品分类数量
    path('statistics/categoryCount', categoryCountView.as_view(), name="statistics_categoryCount"),
    #统计-商品数量
    path('statistics/goodsCount', goodsCountView.as_view(), name="statistics_goodsCount"),
    #统计-订单数量
    path('statistics/ordersCount', ordersCountView.as_view(), name="statistics_ordersCount"),
    #统计-评价数量
    path('statistics/commentsCount', commentsCountView.as_view(), name="statistics_commentsCount"),
    #统计-商品分类数量统计
    path('statistics/goodsCategory', goodsCategoryView.as_view(), name="statistics_goodsCategory"),
    #统计-自行车销量统计图
    path('statistics/orderSalary', orderSalaryView.as_view(), name="statistics_orderSalary"),


    # 自行车收藏
    path('front/collect/update', UpdateCollect.as_view(), name="front_updateproducecollect"),
    path('front/collect/collect/<int:goodsId>/<int:userId>', CheckCollect.as_view(), name="front_checkcollect"),
    path('front/collect/<int:goodsId>/<int:userId>', DeleteCollect.as_view(), name="front_deletecollect"),

    # 修改浏览量
    path('front/goods/views/update/<int:id>', UpdateGoodsViews.as_view(), name="front_goodsupdateviews"),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
