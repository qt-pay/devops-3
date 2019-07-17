from config import DEMO_MODE
from django.http import JsonResponse


IN_DEMO_MODE = DEMO_MODE
SAFE_METHOD = ("GET", "HEAD")


class DemoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if IN_DEMO_MODE and request.method not in SAFE_METHOD:
            return JsonResponse({"message": "In demo mode, only safe method only"})

        return self.get_response(request)
