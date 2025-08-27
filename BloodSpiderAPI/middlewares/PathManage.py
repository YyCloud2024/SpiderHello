# Api中间件层, 所以关于Api的请求都必须经过此中间件
from django.utils.deprecation import MiddlewareMixin
from BloodSpiderWeb.views.urls import urlpatterns as views_urls_urlpatterns
from django.conf import settings

class PathManage(MiddlewareMixin):
    def process_request(self, request):
        # 判断如果是 pc 路径
        if request.path.startswith('/pc/'):
            # 读取 views的urls路由
            request.views_urls_urlpatterns = [{"url": "/pc/" + str(url.pattern), "name": url.name} for url in views_urls_urlpatterns]
            # 当前版本
            request.version = settings.SPIDERHELLO_VERSION
            # 管理员微信
            request.admin_wechat = settings.ADMIN_WECHAT
        # 所有验证通过，确保用户已找到并可用
        return None
    def process_response(self, request, response):

        return response



