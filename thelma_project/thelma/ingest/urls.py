from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IngestTemplateView.as_view(), name='ingest'),
    url(r'^statistics/', views.ArchiveStatistics.as_view(), name='statistics'),
    url(r'begin', views.BeginIngestView.as_view(), name='begin'),
    url(r'status', views.IngestStatusView.as_view(), name='status'),
    url(r'update-schedule', views.UpdateIngestSchedule.as_view(), name="update_schedule"),
]
