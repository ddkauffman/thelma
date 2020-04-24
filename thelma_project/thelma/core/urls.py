from django.conf.urls import url

from thelma.core.views import ProfileTemplateView
from thelma.core.views import APIInfoTemplateView

urlpatterns = [
    url(
        r'profile',
        ProfileTemplateView.as_view(),
        name='profile'
    ),
    url(
        r'api/info',
        APIInfoTemplateView.as_view(),
        name='api_info'
    ),
]
