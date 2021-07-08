from django.urls import path

from apps.configurator import views as conf_views
from libs.routers import SimpleRouter
from . import views as api_views

app_name = "apiv1"

simple_router = SimpleRouter()

simple_router.register(conf_views.ConfiguratorViewSet)
simple_router.register(conf_views.AlgorithmViewSet)

urlpatterns = [
    path("visit-tester/", api_views.VisitTestView.as_view(), name="visit-tester"),
]

urlpatterns += simple_router.get_urls()
