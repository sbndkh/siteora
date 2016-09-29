from django.conf.urls import url

from . import views
from .views import IndexView, RequestListJson, FilterView
from django.contrib.auth.decorators import login_required




urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^(?P<id>\d+)/filter/$', FilterView.as_view(), name="filter_dep"),
    url(r'^filing/$', RequestListJson.as_view(), name="request_list_json"),
    url(r'^login/$', views.login_user),
    url(r'^logout/$', views.logout_user),
    #url(r'^requests/$', views.people),
]