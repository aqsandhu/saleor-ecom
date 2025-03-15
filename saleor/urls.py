"""
URL Configuration for Saleor E-Commerce platform.

This module defines the URL patterns for the Saleor application.
It includes routes for the GraphQL API, digital product downloads,
plugin webhooks, thumbnails and other core functionality.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from .core.views import jwks
from .graphql.api import backend, schema
from .graphql.views import GraphQLView
from .plugins.views import (
    handle_global_plugin_webhook,
    handle_plugin_per_channel_webhook,
    handle_plugin_webhook,
)
from .product.views import digital_product
from .thumbnail.views import handle_thumbnail

urlpatterns = [
    # GraphQL API endpoint
    re_path(
        r"^graphql/$",
        csrf_exempt(GraphQLView.as_view(backend=backend, schema=schema)),
        name="api",
    ),
    # Digital product download endpoint
    re_path(
        r"^digital-download/(?P<token>[0-9A-Za-z_\-]+)/$",
        digital_product,
        name="digital-product",
    ),
    # Channel-specific plugin webhook endpoint
    re_path(
        r"^plugins/channel/(?P<channel_slug>[.0-9A-Za-z_\-]+)/"
        r"(?P<plugin_id>[.0-9A-Za-z_\-]+)/",
        handle_plugin_per_channel_webhook,
        name="plugins-per-channel",
    ),
    # Global plugin webhook endpoint
    re_path(
        r"^plugins/global/(?P<plugin_id>[.0-9A-Za-z_\-]+)/",
        handle_global_plugin_webhook,
        name="plugins-global",
    ),
    # Legacy plugin webhook endpoint
    re_path(
        r"^plugins/(?P<plugin_id>[.0-9A-Za-z_\-]+)/",
        handle_plugin_webhook,
        name="plugins",
    ),
    # Thumbnail generation endpoint
    re_path(
        (
            r"^thumbnail/(?P<instance_id>[.0-9A-Za-z_=\-]+)/(?P<size>\d+)/"
            r"(?:(?P<format>[a-zA-Z]+)/)?"
        ),
        handle_thumbnail,
        name="thumbnail",
    ),
    # JSON Web Key Set endpoint for JWT authentication
    re_path(r"^\.well-known/jwks.json$", jwks, name="jwks"),
]

# Debug-only URLs - only enabled when DEBUG=True
if settings.DEBUG:
    from .core import views

    urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT) + [
        # Serve static files directly during development
        re_path(r"^static/(?P<path>.*)$", serve),
        # Homepage URL for development preview
        re_path(r"^$", views.home, name="home"),
    ]
