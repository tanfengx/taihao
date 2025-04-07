from rest_framework.views import APIView
from business.models import *
from system.models import *
from django.db import connection
from system.utils.json_response import *
from rest_framework import status
from django.core.paginator import Paginator
from system.utils.user import UserToken
from datetime import datetime, timedelta
from django.utils import timezone


# 用户
class UserListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = User.objects.all()
            serializerList = UserSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = User.objects.get(id=pk)
            serializer = UserSerializer(model)
            return SuccessResponse(data=serializer.data)

class UserPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = User.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = UserSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )
								
# 网站公告
class NoticeListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Notice.objects.all()
            serializerList = NoticeSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Notice.objects.get(id=pk)
            serializer = NoticeSerializer(model)
            return SuccessResponse(data=serializer.data)

class NoticePage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Notice.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = NoticeSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )

								
# 根据userId查询用户
class getMemberByUserId(APIView):
    def get(self, request, userId):
        model = Member.objects.filter(user_id=userId).first()
        serializer = MemberSerializer(model)
        return SuccessResponse(data=serializer.data)

class UpdateMember(APIView):
    # 新增/修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = MemberSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")

        try:
            model = Member.objects.get(pk=request.data['id'])
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")
# 根据userId查询商家
class getBusinessByUserId(APIView):
    def get(self, request, userId):
        model = Business.objects.filter(user_id=userId).first()
        serializer = BusinessSerializer(model)
        return SuccessResponse(data=serializer.data)

class UpdateBusiness(APIView):
    # 新增/修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = BusinessSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")

        try:
            model = Business.objects.get(pk=request.data['id'])
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BusinessSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 轮播图
class BannerListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Banner.objects.all()
            serializerList = BannerSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Banner.objects.get(id=pk)
            serializer = BannerSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = BannerSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Banner.objects.get(pk=request.data['id'])
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BannerSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Banner.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class BannerPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Banner.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = BannerSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateBanner(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = BannerSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Banner.objects.get(pk=request.data['id'])
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BannerSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 用户
class MemberListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Member.objects.all()
            serializerList = MemberSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Member.objects.get(id=pk)
            serializer = MemberSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Member.objects.get(pk=request.data['id'])
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Member.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class MemberPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Member.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = MemberSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateMember(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = MemberSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Member.objects.get(pk=request.data['id'])
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 商家
class BusinessListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Business.objects.all()
            serializerList = BusinessSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Business.objects.get(id=pk)
            serializer = BusinessSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = BusinessSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Business.objects.get(pk=request.data['id'])
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BusinessSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Business.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class BusinessPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Business.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = BusinessSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateBusiness(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = BusinessSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Business.objects.get(pk=request.data['id'])
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BusinessSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 商品分类
class CategoryListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Category.objects.all()
            serializerList = CategorySerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Category.objects.get(id=pk)
            serializer = CategorySerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Category.objects.get(pk=request.data['id'])
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Category.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class CategoryPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Category.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = CategorySerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateCategory(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = CategorySerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Category.objects.get(pk=request.data['id'])
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 浏览自行车
class GoodsListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Goods.objects.all()
            serializerList = GoodsSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Goods.objects.get(id=pk)
            serializer = GoodsSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = GoodsSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Goods.objects.get(pk=request.data['id'])
        except Goods.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GoodsSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Goods.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")


# 首页推荐自行车
class GoodsListRecom(APIView):
    # 列表
    def get(self, request , pk=None):
        list = Goods.objects.all().order_by("-views")[:4]
        serializerList = GoodsSerializer(list, many=True)
        return SuccessResponse(data=serializerList.data)

class GoodsPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))
        category_id = request.query_params.get('category_id')

        # 构建查询
        list = Goods.objects.all().order_by('-id')
        list = list.filter(state_radio='审核成功')
        if name:
            list = list.filter(name__icontains=name)
        if category_id:
            list = list.filter(category_id=category_id)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = GoodsSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateGoods(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = GoodsSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Goods.objects.get(pk=request.data['id'])
        except Goods.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GoodsSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 购物车
class CartListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Cart.objects.all()
            serializerList = CartSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Cart.objects.get(id=pk)
            serializer = CartSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Cart.objects.get(pk=request.data['id'])
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Cart.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class CartPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Cart.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = CartSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateCart(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = CartSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Cart.objects.get(pk=request.data['id'])
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 订单评论
class CommentsListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Comments.objects.all()
            serializerList = CommentsSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Comments.objects.get(id=pk)
            serializer = CommentsSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = CommentsSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Comments.objects.get(pk=request.data['id'])
        except Comments.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentsSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Comments.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class CommentsPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Comments.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = CommentsSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateComments(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = CommentsSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Comments.objects.get(pk=request.data['id'])
        except Comments.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentsSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 商品订单
class OrdersListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Orders.objects.all()
            serializerList = OrdersSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Orders.objects.get(id=pk)
            serializer = OrdersSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = OrdersSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Orders.objects.get(pk=request.data['id'])
        except Orders.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrdersSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Orders.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class OrdersPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Orders.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = OrdersSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateOrders(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = OrdersSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Orders.objects.get(pk=request.data['id'])
        except Orders.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrdersSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 支付方式
class PaytypeListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Paytype.objects.all()
            serializerList = PaytypeSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Paytype.objects.get(id=pk)
            serializer = PaytypeSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = PaytypeSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Paytype.objects.get(pk=request.data['id'])
        except Paytype.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PaytypeSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Paytype.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class PaytypePage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Paytype.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = PaytypeSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdatePaytype(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = PaytypeSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Paytype.objects.get(pk=request.data['id'])
        except Paytype.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PaytypeSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 收货地址
class AddressListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Address.objects.all()
            serializerList = AddressSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Address.objects.get(id=pk)
            serializer = AddressSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Address.objects.get(pk=request.data['id'])
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Address.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class AddressPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Address.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = AddressSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateAddress(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = AddressSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Address.objects.get(pk=request.data['id'])
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 自行车收藏
class CollectListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Collect.objects.all()
            serializerList = CollectSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Collect.objects.get(id=pk)
            serializer = CollectSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = CollectSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Collect.objects.get(pk=request.data['id'])
        except Collect.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CollectSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Collect.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class CollectPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Collect.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = CollectSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateCollect(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = CollectSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Collect.objects.get(pk=request.data['id'])
        except Collect.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CollectSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

# 售后服务
class ServicesListDetail(APIView):
    # 列表和查询一个
    def get(self, request , pk=None):
        if pk is None:
            list = Services.objects.all()
            serializerList = ServicesSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Services.objects.get(id=pk)
            serializer = ServicesSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = ServicesSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Services.objects.get(pk=request.data['id'])
        except Services.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ServicesSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Services.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")
		
class ServicesPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Services.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = ServicesSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )

class MyServicesPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        user_id = UserToken.user_id(request)
        list = Services.objects.all().order_by('-id')
        list = list.filter(user_id=user_id)
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = ServicesSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )

class UpdateServices(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = ServicesSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Services.objects.get(pk=request.data['id'])
        except Services.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ServicesSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")


# 添加/修改购物车
class UpdateCart(APIView):
    def post(self, request):
        id = None
        if 'id' in request.data:
            id = request.data['id']
        name = None
        if 'name' in request.data:
            name = request.data['name']
        num = None
        if 'num' in request.data:
            num = request.data['num']
        img = None
        if 'img' in request.data:
            img = request.data['img']
        price = None
        if 'price' in request.data:
            price = request.data['price']
        userId = None
        if 'userId' in request.data:
            userId = request.data['userId']
        if 'goodid' in request.data:
            goodid = request.data['goodid']
        bizUserId = None
        if 'bizUserId' in request.data:
            bizUserId = request.data['bizUserId']
		
        cart = Cart.objects.filter(name=name,user_id=userId).first()
        if cart:
            if id:
                cart.num = num
                cart.save()
            else:
                cart.num = cart.num+num
                cart.save()
            return SuccessResponse(msg="操作成功")
        else:
            Cart.objects.create(
                name=name,
                num=num,
                img=img,
                price=price,
                user_id=userId,
                goodid=goodid,
                biz_user_id=bizUserId
            )
            return SuccessResponse(msg="添加成功")


# 添加/修改收货地址
class UpdateAddress(APIView):
    def post(self, request):
        id = None
        if 'id' in request.data:
            id = request.data['id']
        name = None
        if 'name' in request.data:
            name = request.data['name']
        phone = None
        if 'phone' in request.data:
            phone = request.data['phone']
        address = None
        if 'address' in request.data:
            address = request.data['address']
        postcode = None
        if 'postcode' in request.data:
            postcode = request.data['postcode']
        userId = None
        if 'userId' in request.data:
            userId = request.data['userId']
        defaultRadio = None
        if 'defaultRadio' in request.data:
            defaultRadio = request.data['defaultRadio']

        if id:
            dbAddr = Address.objects.filter(id=id).first()
            if dbAddr:
                dbAddr.name=name
                dbAddr.phone=phone
                dbAddr.address=address
                dbAddr.postcode=postcode
                dbAddr.default_code=defaultRadio
                dbAddr.save()
        else:
            Address.objects.create(
            name=name,
            phone=phone,
            address=address,
            postcode=postcode,
            user_id=userId,
            default_radio=defaultRadio
            )
        return SuccessResponse(msg="操作成功")

# 设置默认收货地址
class UpdateAddressDefault(APIView):
    def put(self, request, pk):
        user_id = UserToken.user_id(request)
        list = Address.objects.filter(user_id=user_id)
        for addr in list:
            addr.default_radio = '否'
            addr.save()

        curAddr = Address.objects.filter(id=pk).first()
        curAddr.default_radio = '是'
        curAddr.save()
        return SuccessResponse(msg="设置成功")

# 添加/修改订单
class UpdateOrders(APIView):
    def post(self, request):
        id = None
        if 'id' in request.data:
            id = request.data['id']
        name = None
        if 'name' in request.data:
            name = request.data['name']
        content = None
        if 'content' in request.data:
            content = request.data['content']
        stateRadio = None
        if 'stateRadio' in request.data:
            stateRadio = request.data['stateRadio']
        userId = None
        if 'userId' in request.data:
            userId = request.data['userId']
        amount = None
        if 'amount' in request.data:
            amount = request.data['amount']
        goodids = None
        if 'goodids' in request.data:
            goodids = request.data['goodids']
        bizUserId = None
        if 'bizUserId' in request.data:
            bizUserId = request.data['bizUserId']

        if id:
            dbOrders = Orders.objects.filter(id=id).first()
            if dbOrders:
                if name is not None:
                    dbOrders.name=name
                if content is not None:
                    dbOrders.content=content
                if stateRadio is not None:
                    dbOrders.state_radio=stateRadio
                if userId is not None:
                    dbOrders.user_id=userId
                if amount is not None:
                    dbOrders.amount=amount
                if goodids is not None:
                    dbOrders.goodids=goodids
                if bizUserId is not None:
                    dbOrders.biz_user_id=bizUserId
                dbOrders.save()
        else:
            Orders.objects.create(
            name=name,
            content=content,
            state_radio=stateRadio,
            user_id=userId,
            amount=amount,
            goodids=goodids,
            biz_user_id=bizUserId,
            )
        return SuccessResponse(msg="操作成功")

# 取消订单
class CancelOrders(APIView):
    def put(self, request, pk):
        curAddr = Orders.objects.filter(id=pk).first()
        curAddr.state_radio = '已取消'
        curAddr.save()
        return SuccessResponse(msg="取消成功")



# 查看订单评价
class CommentsTree(APIView):
    def get(self,request):
        goodsId = request.query_params.get('goodsId')
        user_list = User.objects.all()
        all_user = list(user_list.values())
        comments_all = Comments.objects.filter(goods_id=goodsId)
        comments_all_list = list(comments_all.values())

        # 一级评论
        first_comments = Comments.objects.filter(goods_id=goodsId,pid=None)
        first_comments_list = list(first_comments.values())

        # 给每个评论设置用户
        for comment in first_comments_list:
            user = next((user for user in all_user if user['id'] == comment['user_id']), None)
            comment['user'] = user

        # 二级评论
        for comment in first_comments_list:
            pid = comment['id']
            second_comments = [comment1 for comment1 in comments_all_list if comment1['pid'] == pid]  # 二级评论

            # 二级评论设置用户
            for comment1 in second_comments:
                user = next((user for user in all_user if user['id'] == comment1['user_id']), None)
                puser = next((user for user in all_user if user['id'] == comment1['puser_id']), None)
                comment1['user'] = user
                comment1['puser'] = puser

            comment['children'] = second_comments  # 一级评论设置二级评论

        #驼峰转换
        for comment in first_comments_list:
            convert_props_to_camel_case(comment)

        return SuccessResponse(data=first_comments_list)


# 添加/修改订单评价
class UpdateComments(APIView):
    def post(self, request):
        content = None
        if 'content' in request.data:
            content = request.data['content']
        score = None
        if 'score' in request.data:
            score = request.data['score']
        userId = None
        if 'userId' in request.data:
            userId = request.data['userId']
        goodsId = None
        if 'goodsId' in request.data:
            goodsId = request.data['goodsId']
        pid = None
        if 'pid' in request.data:
            pid = request.data['pid'] 
        puserId = None
        if 'puserId' in request.data:
            puserId = request.data['puserId']   			
        bizUserId = None
        if 'bizUserId' in request.data:
            bizUserId = request.data['bizUserId']
        ordersId = None
        if 'ordersId' in request.data:
            ordersId = request.data['ordersId']
        Comments.objects.create(
			content=content,
			score=score,
			user_id=userId,
			goods_id=goodsId,
			pid=pid,
			puser_id=puserId,
            biz_user_id=bizUserId,
            orders_id=ordersId,
        )
		
        return SuccessResponse(msg="操作成功")



# 统计-商品分类数量
class categoryCountView(APIView):
    def get(self,request):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''

        sql = "select count(*) as categoryCount from category"
        params = None
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result[0])

# 统计-商品数量
class goodsCountView(APIView):
    def get(self,request):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''
        user_id = UserToken.user_id(request)

        sql = "select count(*) as goodsCount from goods where user_id=%s"
        params = (user_id)
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result[0])

# 统计-订单数量
class ordersCountView(APIView):
    def get(self,request):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''
        user_id = UserToken.user_id(request)

        sql = "select count(*) as ordersCount from orders where biz_user_id=%s"
        params = (user_id)
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result[0])

# 统计-评价数量
class commentsCountView(APIView):
    def get(self,request):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''
        user_id = UserToken.user_id(request)

        sql = "select count(*) as commentsCount from comments where biz_user_id=%s"
        params = (user_id)
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result[0])


	
# 统计-商品分类数量统计
class goodsCategoryView(APIView):
    def get(self,request):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''
        user_id = UserToken.user_id(request)

        sql = "SELECT c.name AS `name`,COUNT(c.name) AS `value` FROM goods r INNER JOIN category c WHERE r.user_id=%s and c.id = r.category_id GROUP BY c.name"
        params = (user_id)
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result)

# 统计-自行车销量统计图
class orderSalaryView(APIView):
    def get(self,request):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''

        beginDate = request.query_params.get('beginDate')
        endDate = request.query_params.get('endDate')

        # 当前时间
        now = timezone.now()

        # 如果beginDate为空，则设置为当前时间的前一个月
        if not beginDate:
            beginDate = (now - timedelta(days=30)).strftime('%Y-%m-%d')
        else:
            beginDate = datetime.strptime(beginDate, '%Y-%m-%d').strftime('%Y-%m-%d')

        # 如果beginDate为空，则设置为当前时间的前一个月
        if not beginDate:
            beginDate = (now - timedelta(days=30)).strftime('%Y-%m-%d')
        else:
            beginDate = datetime.strptime(beginDate, '%Y-%m-%d').strftime('%Y-%m-%d')

        # 如果endDate为空，则设置为当前时间加1天
        if not endDate:
            endDate = (now + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            endDate = datetime.strptime(endDate, '%Y-%m-%d').strftime('%Y-%m-%d')

        user_id = UserToken.user_id(request)

        sql = """SELECT DATE_FORMAT(create_time, '%%Y-%%m-%%d') AS `name`,COUNT(amount) AS `value` FROM orders WHERE biz_user_id=%s and DATE_FORMAT(create_time, '%%Y-%%m-%%d') >= %s and DATE_FORMAT(create_time, '%%Y-%%m-%%d')<= %s GROUP BY DATE_FORMAT(create_time, '%%Y-%%m-%%d') ORDER BY DATE_FORMAT(create_time, '%%Y-%%m-%%d')"""

        params = (user_id,beginDate, endDate)
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result)

		


# 修改自行车收藏
class UpdateCollect(APIView):
    # 修改
    def post(self, request):
        id = None
        if 'id' in request.data:
            id = request.data['id']
        userId = None
        if 'userId' in request.data:
            userId = request.data['userId']
        goodsId = None
        if 'goodsId' in request.data:
            goodsId = request.data['goodsId']

        if id:
            dbOne = Collect.objects.filter(id=id).first()
            if dbOne:
                dbOne.user_id = userId
                dbOne.goods_id = goodsId
                dbOne.save()
        else:
            Collect.objects.create(
                user_id=userId,
                goods_id=goodsId
            )
        return SuccessResponse(msg="操作成功")

# 查询自行车收藏
class CheckCollect(APIView):
    def get(self, request, goodsId,userId):
        dbOne = Collect.objects.filter(goods_id=goodsId,user_id=userId).first()
        flag = False
        if dbOne:
            flag = True
        return SuccessResponse(flag)

# 删除自行车收藏
class DeleteCollect(APIView):
    def delete(self, request, goodsId,userId):
        dbOne = Collect.objects.filter(goods_id=goodsId,user_id=userId).first()
        if dbOne:
            dbOne.delete()
        return SuccessResponse(msg="操作成功")

# 修改浏览量
class UpdateGoodsViews(APIView):
    # 修改
    def post(self, request, id):
        dbOne = Goods.objects.filter(id=id).first()
        if dbOne.views:
            dbOne.views = dbOne.views+1
        else:
            dbOne.views = 1
        dbOne.save()
        return SuccessResponse(msg="操作成功")



def to_camel_case(s):
    parts = s.split('_')
    return parts[0] + ''.join(part.title() for part in parts[1:])

def convert_props_to_camel_case(data):
    for key, value in list(data.items()):
        if isinstance(value, dict):
            convert_props_to_camel_case(value)
        elif isinstance(value, list):
            for item in value:
                convert_props_to_camel_case(item)
        camel_case_key = to_camel_case(key)
        data[camel_case_key] = data.pop(key)
