__author__ = 'soheil'
from django.conf.urls import url
from . import views

app_name = 'app1'

urlpatterns = [

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    url(r'^clans/$', views.ClanList.as_view()),
    url(r'^clans/(?P<pk>[0-9]+)/$', views.ClanDetail.as_view()),
    url(r'^clans/(?P<clan_pk>[0-9]+)/(?P<action>[a-z]+)/$', views.ClanMembership.as_view()),

    url(r'^match_request$', views.match_request),
    url(r'^update_match_result$', views.update_match_result),
    url(r'^get_updates$', views.get_updates),
    url(r'^update_username$', views.update_username),
    url(r'^get_leaders$', views.get_leaders),
    url(r'^deck$', views.deck),
    url(r'^card$', views.card),
    url(r'^bug_report$', views.bug_report),
    url(r'^bot_deck$', views.bot_deck),
    url(r'^test$', views.Test.as_view()),
]

