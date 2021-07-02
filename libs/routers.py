class SimpleRouter:
    """简单路由生成器"""

    register_list = []

    def register(self, viewset):
        """将 viewset 注册"""
        self.register_list.append(viewset)
        return self.register_list

    def get_urls(self):
        """生成所有注册的 urlpatterns"""
        urlpatterns = []
        for item in self.register_list:
            urlpatterns.extend(item().get_urls())
        return urlpatterns
