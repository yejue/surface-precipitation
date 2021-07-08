from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from libs.printer import s_print
# Create your views here.


class VisitTestView(View):
    """
    请求测试接口
     - 用于研究请求的出入流程
     - 用于研究请求体的数据格式
    """

    def get(self, request):
        html = []

        # 1 整体请求的打印
        # 分别打印请求对象、请求对象类型、请求对象的 __dir__
        html.append(s_print("整体部分"))

        print(request)
        html.append(str(request))

        print(type(request))
        html.append(str(type(request)))

        print(dir(request))
        html.append(str(dir(request)))

        # 2 请求中 META 部分进行打印
        html.append(s_print("META 部分"))

        print(request.META)
        html.append(str(request.META))

        # 可视化拼接
        html = "<br>".join(html)

        return HttpResponse(html)
