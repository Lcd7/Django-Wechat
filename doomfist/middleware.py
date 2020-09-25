from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.views.debug import technical_500_response
from django.conf import settings

import sys

# 旧方法 因为middlewareMixin即将被删除， 不推荐
# 继承MiddlewareMixin类不会报错
class TestMiddleware(MiddlewareMixin):
    '''
    封禁ip
    '''
    def process_request(self, request):
        print("TestMiddleware处理请求")

    def process_response(self, request, response):
        print("TestMiddleware返回响应")
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if 'HTTP_X_FORWARDED_fOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        if ip in getattr(settings, "BLACKLIST", []):
            return HttpResponse('<h1>你的ip被禁止</h1>')
    
    def process_exception(self, request, exception):
        if 'HTTP_X_FORWARDED_fOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        print("TestMiddleware处理视图异常...")
        if request.user.is_superuser or ip in settings.ADMIN_IP:
            return technical_500_response(request, *sys.exc_info())
        # 如果是其他用户 交给默认的处理流程

# 新方法  推荐
class Md2:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # 在这里编写视图和后面的中间件被调用之前需要执行的代码
        # 这里其实就是旧的process_request()方法的代码
        print("Md2处理请求")

        response = self.get_response(request)

        # 在这里编写视图调用后需要执行的代码
        # 这里其实就是旧的process_response()方法的代码
        print("Md2返回响应")

        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        print(f"Md2在执行{view_func.__name__}视图前")

    def process_exception(self, request, exception):
        print("Md2处理视图异常")   



