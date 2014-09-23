from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'adverts.views.index', name='index'),
    url(r'register/$', 'adverts.views.register'),
    url(r'login/$', 'adverts.views.user_login'),


)
