
from django.conf.urls import include, url
from django.contrib import admin
from . import views


from django.conf.urls.static import static
# from quicky import api
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$',views.login,name='logn'),
    url(r'^pages/(?P<path>.*)$', views.load_page, name='singleshop'),
    url(r'^categories/(?P<path>.*)$', views.load_categories, name='singleshop'),

    url(r'^api$',"quicky.api.call")
    ]
