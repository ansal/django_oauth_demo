from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import api.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_oauth_demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),

    url(r'^api/verify', api.views.verify_token, name='verify' ),
)
