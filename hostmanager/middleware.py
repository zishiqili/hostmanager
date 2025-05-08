import time
from django.utils.deprecation import MiddlewareMixin

class RequestTimingMiddleware(MiddlewareMixin):
    """中间件用于统计请求处理耗时"""
    
    def process_request(self, request):
        """在请求开始时记录时间"""
        request.start_time = time.time()
    
    def process_response(self, request, response):
        # 计算耗时（毫秒）
        total_time = (time.time() - request.start_time) * 1000
        print(total_time)
        response['X-Request-Time'] = f'{total_time:.2f}ms'
        
        return response
