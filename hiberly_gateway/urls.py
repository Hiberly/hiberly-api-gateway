"""hiberly_gateway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import requests
from django.urls import path, re_path, include
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from social_django.models import UserSocialAuth
import json
from oauth2_provider.models import AccessToken  


def gitlab_api_proxy(request, return_request=False):
    if not request.GET.get('access_token'):
        return HttpResponse('No access code provided', status=401)
    user = AccessToken.objects.get(token=request.GET['access_token']).user
    social = user.social_auth.get(provider='gitlab')
    request = requests.get('%s%s?access_token=%s' % (settings.GITLAB_URL, request.path, social.extra_data['access_token']))
    if return_request:
        return request
    return HttpResponse(request.content, content_type="application/json")

def gitlab_changes_proxy(request, **kwargs):
    response = gitlab_api_proxy(request, return_request=True).json()
    for change in response['changes']:
        change['diff'] = 'REDACTED'
    return JsonResponse(response)


urlpatterns = [
    re_path(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include('social_django.urls', namespace='social')),
    path('api/v4/user', gitlab_api_proxy),
    path('api/v4/merge_requests', gitlab_api_proxy),
    path('api/v4/projects/<int:id>', gitlab_api_proxy),
    path('api/v4/projects/<int:id>/merge_requests/<int:merge_request_iid>/changes', gitlab_changes_proxy),
    path('api/v4/projects/<int:id>/merge_requests/<int:merge_request_iid>/notes', gitlab_changes_proxy),
    path('api/v4/projects/<int:id>/merge_requests/<int:merge_request_iid>/notes/<int:notes_id>', gitlab_changes_proxy),
    path('admin/', admin.site.urls),
]
