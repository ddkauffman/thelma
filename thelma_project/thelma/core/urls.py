from django.conf.urls import url

from thelma.core.views import ProfileTemplateView

urlpatterns = [
    url(r'profile', ProfileTemplateView.as_view(), name='profile'),
]
