from django.urls import include, path

"""
This module defines the URL patterns for version 1 of the API.

To add an internal admin API, you can create a new URL pattern with a specific
prefix (e.g., `admin/`) and include the corresponding URL configurations.
Similarly, to add a public API, you can create another URL pattern with a
different prefix (e.g., `public/`) and include the respective URL configurations.

Example:
    path("admin/", include("api.v1.admin.urls", namespace="admin")),
    path("public/", include("api.v1.public.urls", namespace="public")),
"""

app_name = "api-v1"

urlpatterns = [
    path("app/", include("api.v1.app.urls", namespace="app")),
]
