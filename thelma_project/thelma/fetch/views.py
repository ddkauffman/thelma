"""Django View for telemetry fetching

This Django view is responsible for handling requests for telemetry data

"""

import json
import requests

import plotly.plotly as plotly
import plotly.graph_objs  as go
from plotly.offline import plot as pl

from datetime import datetime
from astropy.time import Time

from django.conf import settings

from django.http import HttpResponse

from django.shortcuts import render
from django.views.generic import View
from django.views.generic import TemplateView

from thelma.core.views import get_user_preference


def get_mnemonic_date_range(mnemonic):

    url = f'http://{settings.TELEMETRY_API_HOST}{settings.TELEMETRY_API_PORT}/api/v1/fetch/date-range'

    try:
        date_range = requests.get(url,  params={'mnemonic': mnemonic, })
    except Exception as err:
        raise ValueError(err.args[0])
    if date_range.json().get('error', '') != '':
        raise ValueError(date_range.json().get('error'))
    return date_range.json()


class FetchMnemonicDataInRange(View):
    """Fetch Mnemonic Data In A Date Range

    This class inherits from the generic View class provided by Django The
    only method that is overridden is the get method. HTTP POST is not allowed
    since the application is intended to view and analyze data only.
    """

    def get(self, request):

        mnemonic = request.GET.get('mnemonic').replace(' ', '')
        new_domain_start = request.GET.get('newDomainStart', None)
        new_domain_end = request.GET.get('newDomainEnd', None)

        url = f'http://{settings.TELEMETRY_API_HOST}{settings.TELEMETRY_API_PORT}/api/v1/fetch/data'

        telemetry = requests.get(url, params={
            'mnemonic': mnemonic,
            'newDomainStart': new_domain_start,
            'newDomainEnd': new_domain_end
            })

        return HttpResponse(telemetry, content_type="application/json")


class FetchMnemonicDateRange(View):

    def get(self, request):

        mnemonic = request.GET.get('mnemonic').replace(' ', '')
        try:
            date_range = get_mnemonic_date_range(mnemonic)
        except Exception as err:
            self.status = 400
            return HttpResponse(
                    json.dumps({'error': str(err.args[0])}),
                    status=self.status,
                    content_type="application/json"
            )

        return HttpResponse(date_range, content_type="application/json")


class FetchMnemonicData(View):

    def __init__(self):
        self.status = 200

    def get(self, request):

        try:
            mnemonic = request.GET.get('mnemonic').replace(' ', '')
            if mnemonic == '':
                raise ValueError('Oops! Sorry, missing parameter, mnenonic.')
            date_range = get_mnemonic_date_range(mnemonic)

            start_of_range = request.GET.get('start_of_range').replace(' ', '')

            if start_of_range == '':
                start_of_range = Time(date_range['date_range'][0], format='iso').yday

            end_of_range = request.GET.get('end_of_range').replace(' ', '')

            url = f'http://{settings.TELEMETRY_API_HOST}{settings.TELEMETRY_API_PORT}/api/v1/fetch/plot'

            telemetry = requests.get(url,  params={
                    'mnemonic': mnemonic,
                    'start_of_range': start_of_range,
                    'end_of_range': end_of_range
                }
            )
        except Exception as err:
            self.status = 400
            return HttpResponse(
                    json.dumps({'error': str(err.args[0])}),
                    status=self.status,
                    content_type="application/json"
                   )

        return HttpResponse(
                    telemetry,
                    status=200,
                    content_type="application/json"
                )


class FiveMinStats(TemplateView):

    def get(self, request):

        statistics = []
        mnemonic = request.GET.get('mnemonic', None)

        if mnemonic is not None and mnemonic != 'default':

            url = f'http://{settings.TELEMETRY_API_HOST}{settings.TELEMETRY_API_PORT}/api/v1/fetch/stats'
            parameters = {'mnemonic': mnemonic, 'interval': '5min'}

            try:
                statistics = requests.get(url,  params=parameters)
                statistics = statistics.json()['stats']
            except Exception as err:
                return HttpResponse(json.dumps({
                    'message': err.args[0],
                    'source': 'thelman.web',
                    'class': FiveMinStats,
                    'call_response': statistics
                    }), status=500, content_type="application/json")

        return render(
            request,
            'fetch/stats/5min_stats.html',
            {'statistics': statistics}
        )


class DailyStats(TemplateView):

    def get(self, request):

        statistics = []
        mnemonic = request.GET.get('mnemonic', None)

        if mnemonic is not None and mnemonic != 'default':

            url = f'http://{settings.TELEMETRY_API_HOST}{settings.TELEMETRY_API_PORT}/api/v1/fetch/stats'
            parameters = {'mnemonic': mnemonic, 'interval': 'daily'}

            try:
                pass
            except Exception as err:
                return HttpResponse(json.dumps({'message': err.args[0]}), status=500, content_type="application/json")

        return render(
            request,
            'fetch/stats/daily_stats.html',
            {'statistics': statistics}
        )


class FetchStatisticsMinMeanMaxPlot(View):

    def create_plot_markup(self, statistics):

        # TODO: Refactor this to encapsulate what changes and follow naming convention.
        random_x = statistics['times']
        random_y0 = statistics['mins']
        random_y1 = statistics['means']
        random_y2 = statistics['maxes']

        # Create traces
        marker_faded = dict({
            'color':  'rgb(192, 192, 192)',
            'line': {
                'color': 'rgb(224, 224, 224)',
                },
        })

        marker_highlight = dict({
            'color':  'rgb(255, 51, 51)',
            'line': {
                'color': 'rgb(255, 102, 102)',
                },
        })

        min = go.Scatter({'x': random_x, 'y': random_y0, 'mode': 'lines+markers', 'name': 'min', 'marker': marker_faded})
        mean = go.Scatter({'x': random_x, 'y': random_y1, 'mode': 'lines+markers', 'name': 'mean', 'marker': marker_highlight})
        max = go.Scatter({'x': random_x, 'y': random_y2, 'mode': 'lines+markers', 'name': 'max', 'marker': marker_faded})

        data = [min, mean, max]
        layout = go.layout = go.Layout(title='5min Statistics')

        fig = go.Figure(data=data, layout=layout)

        return pl(fig, output_type='div', include_plotlyjs=False)

    def get(self, request):

        url = (
            f'http://{settings.TELEMETRY_API_HOST}'
            f':{settings.TELEMETRY_API_PORT}'
            f'/api/v1/fetch/min-mean-max'
        )

        response = requests.get(
                        url,
                        params={
                            'mnemonic': request.GET.get('mnemonic'),
                        }
                    )

        statistics = response.json()['data']

        return HttpResponse(self.create_plot_markup(statistics))


class FetchTemplateView(TemplateView):

    def get(self, request):

        return render(
            request,
            'fetch/index.html',
            {
                'activate_application': 'fetch',
                'user_preferences': get_user_preference(request),

            }
        )
