from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bureau_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url='/admin/', permanent=False)),

    url(r'^admin/edda/humen/(?P<pk>\d+)/do-check-in-quartiere/', "edda.views.humen_do_check_in_quartiere"),
    url(r'^admin/edda/humen/(?P<pk>\d+)/do-set-retired-quartiere/', "edda.views.humen_do_set_retired_quartiere"),
    url(r'^admin/edda/humen/(?P<pk>\d+)/do-set-null-arrived-quartiere/', "edda.views.humen_do_set_null_arrived_quartiere"),
    url(r'^admin/edda/humen/(?P<pk>\d+)/do-prepare-substitution/', "edda.views.humen_do_prepare_substitution"),
    url(r'^admin/edda/humen/(?P<pk>\d+)/do-humen-print-badge/', "edda.views.humen_do_print_badge"),
    url(r'^admin/edda/humen/(?P<pk>\d+)/do-change-password/', "edda.views.change_humen_password"),
    url(r'^admin/edda/humen/(?P<pk>\d+)/get-posix-groups/', "edda.views.get_posix_groups"),
    url(r'^admin/edda/humen/(?P<pk>\d+)/increment-badge/', "edda.views.humen_increment_badge"),

    url(r'^admin/edda/vclans/(?P<pk>\d+)/do-check-in-campo/', "edda.views.vclans_do_check_in_campo"),
    url(r'^admin/edda/vclans/(?P<pk>\d+)/do-check-in-quartiere/', "edda.views.vclans_do_check_in_quartiere"),
    url(r'^admin/edda/vclans/(?P<pk>\d+)/do-check-in-quartiere-vclan/', "edda.views.vclans_do_check_in_quartiere_vclan"),
    url(r'^admin/edda/vclans/(?P<pk>\d+)/do-set-retired-campo/', "edda.views.vclans_do_set_retired_campo"),
    url(r'^admin/edda/vclans/(?P<pk>\d+)/do-set-null-arrived-campo/', "edda.views.vclan_do_set_null_arrived_campo"),
    url(r'^admin/edda/vclans/(?P<pk>\d+)/do-set-null-arrived-quartiere/', "edda.views.vclan_do_set_null_arrived_quartiere"),
    url(r'^admin/edda/vclans/(?P<pk>\d+)/do-set-null-arrived-quartiere-vclan/', "edda.views.vclan_do_set_null_arrived_quartiere_vclan"),
    url(r'^admin/edda/vclans/(?P<pk>\d+)/do-vclan-print-badge/', "edda.views.vclan_do_print_badge"),
    url(r'^admin/', include(admin.site.urls)),

    url(r'api/vclans-list/', 'edda.views.api_vclans_list'),
    url(r'api/search-vclan/', 'edda.views.api_search_vclan'),
    url(r'api/set-vclan-arrived/', 'edda.views.api_set_vclan_arrived'),
    url(r'check-in/', 'edda.views.check_in'),
)
