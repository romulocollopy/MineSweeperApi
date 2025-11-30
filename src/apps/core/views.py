from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.generic import View


class CSRFView(View):
    def get(self, request):
        return JsonResponse(dict(csrf_token=get_token(request)))
