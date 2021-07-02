from apps.configurator import views as conf_views
from libs.routers import SimpleRouter

app_name = "apiv1"

simple_router = SimpleRouter()

simple_router.register(conf_views.ConfiguratorViewSet)
simple_router.register(conf_views.AlgorithmViewSet)

urlpatterns = []

urlpatterns += simple_router.get_urls()
