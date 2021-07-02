from rest_framework.viewsets import ModelViewSet

from libs.response import json_response


class CustomModelViewSet(ModelViewSet):
    """定制化 ModelViewSet"""

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return json_response(data=response.data, status=response.status_code)
