from django.urls import URLPattern, include, path
from . import devUrls, userUrls


urlpatterns = [
    path('user/', include(userUrls)),
    path('dev/', include(devUrls))
]