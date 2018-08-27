from django.conf.urls import url
from . import views
app_name='todoapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>[0-9]+)/$',views.description,name='description'),
]