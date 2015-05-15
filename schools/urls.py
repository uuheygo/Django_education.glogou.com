from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'schools.views.list_view', name = 'full_list'),
    url(r'^page=(?P<page>\d+)/$', 'schools.views.list_view', name = 'page_list'),
    url(r'^school_id=(?P<school_id>\d+)/.+/media/$', 
        'schools.views.media_view', name = 'school_media'), # media details: search engine, site, language, social media
    url(r'^school_id=(?P<school_id>\d+)/.+/info/$', 
        'schools.views.info_view', name = 'school_info'),
    url(r'^school_id=(?P<school_id>\d+)/.+/news/$', 
        'schools.views.news_view', name = 'school_news'),
    url(r'^school_id=(?P<school_id>\d+)/.+/report/$', 
        'schools.views.report_view', name = 'school_report'),
    url(r'^school_id=(?P<this_id>\d+)/.+/compare/$', 'schools.views.compare_view', name = 'school_comparison'),
    url(r'^school_id=(?P<school_id>\d+)/.+/$', 
        'schools.views.school_view', name = 'school_page'),
    url(r'^custom_selection/$', 'schools.views.custom_selection', name = 'custom_selection'), # custom selection of schools
    url(r'^contact_us/$', 'schools.views.contact_view'),
]
