from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
   # Examples:
   # url(r'^$', 'generalServer.views.home', name='home'),
   # url(r'^blog/', include('blog.urls')),
   url(r'^rest-auth/', include('rest_auth.urls')),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^rest/', include('app1.urls'))

]
