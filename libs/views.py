import json

from django.db.models import Model
from django.db.utils import IntegrityError
from django.urls import path
from rest_framework.views import APIView

from libs.response import json_response
from libs.res_code import Code, error_map


class SimpleAPIViewRoot:
    """APIView 基础工具类"""

    operation_fields = []   # 设置需要操作的字段，用于过滤与默认序列化
    model = Model           # 设置一个空模型
    request = None          # 设置一个空 request, 仅作为防黄条的美观使用, 与其余视图结合时不考虑 request 的手动设置

    def get_model(self):
        """设置模型类"""
        if not hasattr(self, "model"):
            raise ValueError("未设置表模型")
        if isinstance(self.model, Model):
            raise TypeError("模型类型设置错误")
        return self.model

    def filter(self, queryset):
        """简易过滤器"""
        filter_dict = {}
        for field in self.operation_fields:
            temp = self.request.GET.get(field)
            if temp:
                filter_dict.update({field: temp})

        queryset = queryset.filter(**filter_dict)
        return queryset

    def serializer(self, queryset):
        """简易序列化器"""
        data = []

        for item in queryset:
            temp = {}
            for field in self.operation_fields:
                if field is None:
                    continue
                temp.update({field: item.__dict__[field]})
            data.append(temp)
        return data


class SimpleAPIView(SimpleAPIViewRoot, APIView):
    """
    定制化 APIView
     - 便捷返回模型查询集
     - 便捷参数过滤
    """
    def get(self, request):
        queryset = self.model.objects.all()
        queryset = self.filter(queryset)
        data = self.serializer(queryset)
        return json_response(data=data)

    def post(self, request):
        body = self.request.body
        data = json.loads(body)
        try:
            self.model.objects.create(**data)
        except IntegrityError as e:
            return json_response(result_code=Code.UNIQUEERR, message=f'{error_map[Code.UNIQUEERR]} {e}')
        except Exception as e:
            return json_response(result_code=Code.UNKOWNERR, message=f'{error_map[Code.UNKOWNERR]} {e}')
        return json_response()


class SimpleAPIViewWithID(SimpleAPIViewRoot, APIView):
    """
    定制化 APIView 组件2
     - 对 id 路由进行响应
     - 提供改、查、删数据库接口
    """
    def get(self, request, pk):
        queryset = self.model.objects.filter(id=pk)
        data = self.serializer(queryset)
        return json_response(data=data)

    def put(self, request, pk):
        queryset = self.model.objects.filter(id=pk)

        body = self.request.body
        data = json.loads(body)

        try:
            queryset.update(**data)
        except IntegrityError as e:
            return json_response(result_code=Code.UNIQUEERR, message=f'{error_map[Code.UNIQUEERR]} {e}')
        except Exception as e:
            return json_response(result_code=Code.UNKOWNERR, message=f'{error_map[Code.UNKOWNERR]} {e}')
        return json_response()

    def delete(self, request, pk):
        model = self.get_model()

        try:
            instance = model.objects.get(id=pk)
            instance.delete()
            return json_response(message="删除成功")
        except self.model.DoesNotExist as e:
            return json_response(result_code=Code.NODATA, message=f'{error_map[Code.NODATA]} {e}')
        except Exception as e:
            print(e)
            return json_response(result_code=Code.UNKOWNERR, message=f'{error_map[Code.UNKOWNERR]} {e}')


class SimpleViewSet(SimpleAPIViewRoot):
    """简单视图集"""

    simple_api_view = SimpleAPIView
    simple_api_view_with_id = SimpleAPIViewWithID
    base_name = str

    def __init__(self, *args):
        # 初始化生成两种视图, 以备 get_urls 正常使用
        self.simple_api_view = self.generic_view(SimpleAPIView, "SimpleAPIViewShadow")
        self.simple_api_view_with_id = self.generic_view(SimpleAPIViewWithID, "SimpleAPIViewWithIDShadow")

    def get_urls(self):
        """返回所需 urlpatterns"""
        urlpatterns = [
            path(f"{self.base_name}/", self.simple_api_view().as_view(), name="list"),
            path(f"{self.base_name}/<int:pk>/", self.simple_api_view_with_id().as_view(), name="detail"),
        ]
        return urlpatterns

    def generic_view(self, view, view_name):
        """生成 view 类"""
        model = self.get_model()
        fields = self.operation_fields
        cls = type(view_name, (view, ), dict(model=model, operation_fields=fields))
        return cls
