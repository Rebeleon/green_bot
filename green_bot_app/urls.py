from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'webhook/$', views.pass_update, name='pass_update'),
]
