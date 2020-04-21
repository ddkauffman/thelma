from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.FetchTemplateView.as_view(),
        name='viewer'
    ),
    url(
        r'mnemonic-data/',
        views.FetchMnemonicData.as_view(),
        name='mnemonic'
    ),
    url(
        r'^mnenmoic-range/',
        views.FetchMnemonicDataInRange.as_view(),
        name='range'
    ),
    url(
        r'^mnenmoic-date-range/',
        views.FetchMnemonicDateRange.as_view(),
        name='dates'
    ),
    url(
        r'^5min-stats-markup/',
        views.FiveMinStats.as_view(),
        name='5min-stats-markup'
    ),
    url(
        r'^daily-stats-markup/',
        views.DailyStats.as_view(),
        name='daily-stats-markup'
    ),
    url(
        r'^stats-plot/',
        views.FetchStatisticsMinMeanMaxPlot.as_view(),
        name='stats-plot'
    ),
    url(
        r'default/viewport',
        views.get_default_plot_viewer_content,
        name='default_viewport'
    ),
]
