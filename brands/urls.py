from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'brands.views.list_view', name = 'full_list'),
    url(r'^page=(?P<page>\d+)/$', 'brands.views.list_view', name = 'page_list'),
    url(r'^brand_id=(?P<brand_id>\d+)/.+/media/$',
        'brands.views.media_view', name = 'brand_media'), # media details: search engine, site, language, social media
    url(r'^brand_id=(?P<brand_id>\d+)/.+/info/$',
        'brands.views.info_view', name = 'brand_info'),
    url(r'^brand_id=(?P<brand_id>\d+)/.+/news/$',
        'brands.views.news_view', name = 'brand_news'),
    url(r'^brand_id=(?P<brand_id>\d+)/.+/report/$',
        'brands.views.report_view', name = 'brand_report'),
    url(r'^brand_id=(?P<this_id>\d+)/.+/compare/$', 'brands.views.compare_view', name = 'brand_comparison'),
    url(r'^brand_id=(?P<brand_id>\d+)/.+/$',
        'brands.views.brand_view', name = 'brand_page'),
    url(r'^custom_selection/$', 'brands.views.custom_selection', name = 'custom_selection'), # custom selection of brands
    url(r'^contact_us/$', 'brands.views.contact_view'),
]
