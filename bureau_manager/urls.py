from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bureau_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url='/admin/', permanent=False)),

    url(r'^admin/edda/vclans/(?P<pk>\d+)/do-check-in-campo/', "edda.views.vclans_do_check_in_campo"),
    url(r'^admin/edda/vclans/(?P<pk>\d+)/do-check-in-quartiere/', "edda.views.vclans_do_check_in_quartiere"),
    url(r'^admin/', include(admin.site.urls)),
)
