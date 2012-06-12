from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('avatar.views',
    # url(r'^', include('avatar.urls')),
    url(r'^admin/avatar/parts/(?P<id>\d+)/set_default/?$', 'set_default_part',
        name='set_default_part'),
)
