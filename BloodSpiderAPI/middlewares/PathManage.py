# Api中间件层, 所以关于Api的请求都必须经过此中间件
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class PathManage(MiddlewareMixin):
    def process_request(self, request):
        return None

    def process_response(self, request, response):
        return response



