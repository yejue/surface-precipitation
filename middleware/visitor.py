import logging
from django.utils.deprecation import MiddlewareMixin

visitor_logger = logging.getLogger("visitor")


class GuestOperationMiddleware(MiddlewareMixin):
    """对来访者的操作"""

    def process_request(self, request):
        # 对ip进行记录
        ip = request.META["REMOTE_ADDR"]
        setattr(request, "visit_ip", ip)
        visitor_logger.info(f'{ip} 访问')
