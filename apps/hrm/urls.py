from django.conf.urls import include, url
from django.contrib import admin
from . import views
import quicky
from django.conf.urls.static import static
import os
app=quicky.applications.get_app_by_file(__file__)
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^login$',views.login,name='logn'),
    url(r'^pages/(?P<path>.*)$', views.load_page, name='singleshop'),
    url(r'^categories/(?P<path>.*)$', views.load_categories, name='singleshop'),
    url(r'^category/(?P<path>.*)$', views.load_category),
    url(r'^api$', views.api),
    app.get_static_urls()
    # url(r'^sign_out',views.sign_out)
]

