__author__ = 'soheil'
from django.conf.urls import url
from . import views
from . import clanViews
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

app_name = 'app1'

urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    # url(r'^clans/$', clanViews.ClanList.as_view()),
    # url(r'^clans/(?P<pk>[0-9]+)/$', clanViews.ClanDetail.as_view()),
    # url(r'^clans/(?P<clan_pk>[0-9]+)/(?P<action>[a-z]+)/$', clanViews.ClanMember.as_view()),

    url(r'^match_request$', views.match_request),
    url(r'^update_match_result$', views.update_match_result),
    url(r'^get_updates$', views.get_updates),
    url(r'^update_username$', views.update_username),
    url(r'^get_leaders$', views.get_leaders),
    url(r'^deck$', views.deck),
    url(r'^bug_report$', views.bug_report),
    url(r'^bot_deck$', views.bot_deck),

    #   register new user
    url(r'^v2/users/$', views.UserList.as_view()),
    #   get other user info
    url(r'^v2/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    #   set username
    url(r'^v2/me/username/$', views.SetUsername.as_view()),
    #   get my user info
    url(r'^v2/me/$', views.Me.as_view()),

    url(r'^v2/me/addgem/$', views.AddGem.as_view()),

    # search clan by name
    url(r'^v2/clans/search/(?P<query>[a-zA-z1-9]+)/$', clanViews.SearchClanByName.as_view()),
    # advanced search clan by name
    url(r'^v2/clans/asearch/$', clanViews.AdvancedSearchClan.as_view()),
    #   create new clan
    url(r'^v2/clans/$', clanViews.ClanList.as_view()),
    #   get my clan Profile
    url(r'v2/clans/my/$', clanViews.MyClanDetail.as_view()),
    #   get clan info
    url(r'^v2/clans/(?P<pk>[0-9]+)/$', clanViews.ClanDetail.as_view()),
    #   join/leave clan
    url(r'^v2/clans/(?P<clan_pk>[0-9]+)/(?P<action>[a-z]+)/$', clanViews.ClanMembership.as_view()),

    #   update match result
    url(r'^v2/rooms/(?P<roomID>[a-z0-9]+)/result/$', views.MatchResult.as_view()),

    #   unpack reward pack
    url(r'^v2/packs/(?P<reward_pk>[0-9]+)/unpack/$', views.UnpackReward.as_view()),
    #   unlock reward pack
    url(r'^v2/packs/(?P<reward_pk>[0-9]+)/unlock/$', views.UnlockPack.as_view()),

    #   card upgrade
    url(r'^v2/cards/(?P<cardID>[0-9]+)/$', views.CardUpgrade.as_view()),

    #   donate request
    url(r'v2/donates/$', clanViews.DonateRequest.as_view()),
    #   donate card
    url(r'v2/donates/(?P<donate_pk>[0-9]+)/$', clanViews.Donate.as_view()),
    #   promote user
    url(r'^v2/promote/$', clanViews.PromoteUser.as_view()),
    #   demote user
    url(r'^v2/demote/$', clanViews.DemoteUser.as_view()),
    #   accept user
    url(r'^v2/accept/$', clanViews.AcceptUser.as_view()),
    #   declined user
    url(r'^v2/decline/$', clanViews.DeclineUser.as_view()),
    #   invite user
    url(r'^v2/invite/$', clanViews.InviteUser.as_view()),
    #   kick member
    url(r'v2/kick/$', clanViews.KickMember.as_view()),


]

