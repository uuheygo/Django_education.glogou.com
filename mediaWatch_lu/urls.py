from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView, TemplateView

urlpatterns = [
    # Examples:
    # url(r'^$', 'media_watch_education_lu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('schools.urls')),

    # Add this line for robots.txt, one main reason is that, we do not want search engine to index
    # our testing server. NOTE, we will not check-in robots.txt to github, because
    # production server and testing server will have different robots.txt file.
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt",  content_type='text/plain')),
]
