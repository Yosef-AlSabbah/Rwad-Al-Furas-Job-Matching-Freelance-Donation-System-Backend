"""
URL configuration for Rawad Al Furas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views.decorators.http import require_http_methods
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for load balancers and monitoring."""
    return JsonResponse(
        {"status": "healthy", "service": "Rawad Al Furas API", "version": "1.0.0"}
    )


@require_http_methods(["GET"])
def api_root(request):
    """API root endpoint with available endpoints."""
    return JsonResponse(
        {
            "message": "Welcome to Rawad Al Furas API",
            "version": "1.0.0",
            "endpoints": {
                "auth": "/api/auth/",
                "docs": "/api/docs/",
                "health": "/health/",
                "admin": "/admin/",
            },
        }
    )


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Health check
    path("health/", health_check, name="health_check"),
    # API root
    path("api/", api_root, name="api_root"),
    # Authentication
    path(
        "api/auth/",
        include(
            [
                path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
                path(
                    "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
                ),
                path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
                path("", include("djoser.urls")),
                path("", include("djoser.urls.jwt")),
            ]
        ),
    ),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Your app URLs will go here
    # path("api/jobs/", include("jobs.urls")),
    # path("api/freelance/", include("freelance.urls")),
    # path("api/donations/", include("donations.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Debug Toolbar
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

# Custom admin configuration
admin.site.site_header = "Rawad Al Furas Administration"
admin.site.site_title = "Rawad Al Furas Admin"
admin.site.index_title = "Welcome to Rawad Al Furas Administration"
