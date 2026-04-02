import time
from django.utils.timezone import now


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        user = request.user.username if request.user.is_authenticated else "Anonymous"

        log_message = f'[{now().strftime('%Y-%m-%d %H:%M:%S')}] {request.method} {request.path} - {response.status_code} - {duration:3f}s - {user}'

        print(log_message)

        return response