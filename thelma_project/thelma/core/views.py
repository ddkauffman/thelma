import requests

from django.conf import settings

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import UserForm, ProfileForm
from .models import Profile


night_mode_map = {
    False: 'checked',
    True: '',
}


def get_user_preference(request):

    auth_user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=auth_user.id)
    print(getattr(profile, 'night_mode'))

    return {'daylight_mode': night_mode_map[getattr(profile, 'night_mode')]}


class APIInfoTemplateView(TemplateView):

    def get(self, request):

        URL = f'http://libertyprime.local.stsci.edu:9232/api/v1/info'

        headers = {'Authorization': f'Bearer {settings.API_ACCESS_TOKEN}'}

        response = requests.get(URL, headers=headers).json()
        app = {
            'version': settings.SEMANTIC_VERSION
        }

        context = {
            'api': response,
            'app': app
        }

        return render(request, 'core/api_info.html', context)


class ProfileTemplateView(TemplateView):

    def get(self, request):

        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        return render(request, 'core/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request):

        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        auth_user = User.objects.get(username=request.user)
        u = UserForm(request.POST, instance=auth_user)
        u.save()

        profile = Profile.objects.get(user=auth_user.id)
        f = ProfileForm(request.POST, instance=profile)
        f.save()

        return HttpResponseRedirect(request, 'core/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })
