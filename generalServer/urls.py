from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

urlpatterns = [
   url(r'^api-token-auth/', obtain_jwt_token),
   url(r'^api-token-verify', verify_jwt_token),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^rest/', include('app1.urls')),
]
