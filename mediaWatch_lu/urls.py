from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'media_watch_education_lu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^schools/$', 'schools.views.list_view', name = 'full_list'),
    url(r'^schools/page=(?P<page>\d+)/$', 'schools.views.list_view', name = 'page_list'),
    url(r'^schools/state=(?P<state>\w+)/rank_range=(?P<rank_range>\w+)/page=(?P<page>\d+)/$', 'schools.views.list_view', name = 'selected_list'),
    url(r'^schools/school_id=(?P<school_id>\d+)/$', 'schools.views.school_view', name = 'school_page')
]
