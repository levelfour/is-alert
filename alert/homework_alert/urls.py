from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^done$', views.done, name='done'),
    url(r'^turn$', views.turn, name='turn'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
]
