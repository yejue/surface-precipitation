from rest_framework import serializers

from apps.configurator.models import ConfigModel


class ConfigSerializer(serializers.ModelSerializer):
    """配置表视图序列化器"""

    class Meta:
        model = ConfigModel
        fields = ["id", "config_name", "config_code", "config_body", "remarks"]
