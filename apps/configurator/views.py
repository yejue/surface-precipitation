from apps.configurator.models import ConfigModel, AlgorithmModel
from libs.views import SimpleViewSet
# Create your views here.


class ConfiguratorViewSet(SimpleViewSet):
    """
    配置表视图集合
     - uri: /api/configuration/
     - uri: /api/configuration/:pk/
    """
    model = ConfigModel
    operation_fields = ["id", "config_name", "config_code", "config_body", "remarks"]
    base_name = "configuration"


class AlgorithmViewSet(SimpleViewSet):
    """
    算法表视图集合
     - uri: /api/algorithm/
     - uri: /api/algorithm/
    """
    model = AlgorithmModel
    operation_fields = ["id", "algorithm_name", "algorithm_code", "qc_code", "is_stop"]
    base_name = "algorithm"
