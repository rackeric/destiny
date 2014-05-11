from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'destiny.views.home', name='home'),
    # url(r'^destiny/', include('destiny.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r"^$", 'dcelery.views.test_async'),
    #url(r"^ansible_jeneric/(?P<user_id>\d+)/(?P<job_id>-.*-*.*)", 'dcelery.views.ansible_jeneric_view'),
    #url(r"^ansible_jeneric_testing/(?P<job_id>-.*-*.*)", 'dcelery.views.ansible_jeneric_testing_view'),
    
    # celery stand alone
    url(r"^ansible_jeneric/(?P<user_id>\d+)/(?P<job_id>-.*-*.*)", 'destiny.celery.ansible_jeneric_view'),
)
