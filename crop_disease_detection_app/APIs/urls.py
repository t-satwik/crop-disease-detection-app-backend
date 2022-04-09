from django.urls import URLPattern, include, path
from . import devUrls, userUrls, pageUrls


urlpatterns = [
    path('apis/', include(userUrls)),
    path('dev/', include(devUrls)),
    path('', include(pageUrls)),
]