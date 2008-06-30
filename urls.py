from django.conf.urls.defaults import *
from settings import MEDIA_ROOT

urlpatterns = patterns('',
     (r'^static/(.+)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
     (r'^$', 'views.index'),
     (r'^clean$', 'views.clean'),
     (r'^api/clean$', 'views.clean_api'),
     (r'^about$', 'views.about'),
     (r'^api$', 'views.about_api'),
)
