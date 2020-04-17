import json
import requests
import ntpath

from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import View
from django.views.generic import TemplateView


class UpdateIngestSchedule(View):

    def post(self, request):

        requests.post(f'http://{settings.TELEMETRY_API_HOST}{settings.TELEMETRY_API_PORT}/ingest/update-schedule')

        return HttpResponse(json.dumps({'update schedule': 'success'}), status=200, content_type='application/json')


class IngestStatusView(View):

    def get(self, request):

        response = requests.get(f'http://{settings.TELEMETRY_API_HOST}{settings.TELEMETRY_API_PORT}/ingest/status', params={'task_id': request.GET.get('task_id', 1)})

        return HttpResponse(response, content_type='application/json')


class BeginIngestView(View):

    def __init__(self):
        self.status = 200

    def post(self, request):

        response = requests.post(f'http://{settings.TELEMETRY_API_HOST}{settings.TELEMETRY_API_PORT}/ingest/execute').json()

        return HttpResponse(response)


class ArchiveStatistics(View):

    def get(self, request):

        response = requests.get(f'http://{settings.TELEMETRY_API_HOST}{settings.TELEMETRY_API_PORT}/archive/metrics').json()

        return HttpResponse(response, status="200", content_type="application/json")


class IngestTemplateView(TemplateView):

    def get(self, request):

        return render(request, 'ingest/index.html', {})
