# Inspiration:
# Source - https://stackoverflow.com/questions/78992398/marking-a-cookie-as-partitioned-in-django
# Posted by Vegard
# Retrieved 2025-12-01, License - CC BY-SA 4.0

# Author: Terence Honles

from http import cookies
from django.conf import settings

cookies.Morsel._flags.add("partitioned")
cookies.Morsel._reserved.setdefault("partitioned", "Partitioned")


class CookiePartitioningMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)

        for name in (
            getattr(settings, f"{prefix}_COOKIE_NAME")
            for prefix in ("CSRF", "SESSION", "LANGUAGE")
            if getattr(settings, f"{prefix}_COOKIE_SECURE")
        ):
            if cookie := response.cookies.get(name):
                cookie["Partitioned"] = True

        return response
