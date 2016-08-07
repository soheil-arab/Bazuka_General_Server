__author__ = 'soheil'

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from app1 import serializers as serializer
from app1.models import User, Card, CardType, Clan, UserClanData, RewardPack, Donation
from app1.clanConf import DonationConf
import requests as requests
import time
import json



class ClanMembership(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request, clan_pk, action):
        if action == "join":
            user = request.user.user

            if user.level < 3:
                return Response({'detail': 'Clans unlocks at level 3'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            clan = Clan.get_object(clan_pk)

            if user.trophiesCount < clan.clanMinimumTrophies:
                return Response({'detail': 'Minimum Trophy to join clan is {0}'.format(clan.clanMinimumTrophies)},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            if clan.users.count() >= 50:
                return Response({'detail': 'clan already has 50 members'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if clan.clanType == 2:
                return Response({'detail': 'this is an invite only clan :D'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            elif clan.clanType == 0:
                user.userClan = clan
                # TODO: update score and other things
                if user.clanData is None:
                    clan_data = UserClanData.objects.create()
                    user.clanData = clan_data
                user.save()
                clan_data = serializer.ClanSerializer(clan).data
                return Response(clan_data, status=status.HTTP_201_CREATED)
            elif clan.clanType == 1:
                data = {'time': int(time.time()), 'username': user.username}
                clan.waiting_list[str(user.idUser)] = json.dumps(data)
                clan.save()
                user.pending_clan_id = clan.idClan
                user.save()
        if action == "leave":
            user = request.user.user
            # clan = Clan.get_object(pk=clan_pk)
            if user.clanData.position != 3:
                user.userClan = None
                # TODO: update score and other things
                user.clanData.donate_count = 0
                user.clanData.lastRequestTime = 0
                user.clanData.position = 0
                user.clanData.save()
                user.save()
                return Response({}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': "clanLeader can not leave the clan"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': "invalid action"}, status=status.HTTP_400_BAD_REQUEST)


class Donate(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request, donate_pk):
        user = request.user.user

        donate_obj = Donation.objects.get(pk=donate_pk)
        if donate_obj.requiredCardCount == donate_obj.donatedCardCount:
            return Response({'detail': 'donate done : {0}/{1}'.format(donate_obj.donatedCardCount,
                                                                      donate_obj.requiredCardCount)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        user_donate_count = donate_obj.donators.get(str(user.idUser))
        daily_limit = DonationConf.daily_limit(user.leagueLevel)
        if user.clanData.daily_donate_count >= daily_limit:
            return Response({'detail': 'you can\'t donate more cards'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if user_donate_count is not None:
            max_donate = DonationConf.max_donate_count(user.leagueLevel, donate_obj.cardType.cardRarity)
            if int(user_donate_count) >= max_donate:
                return Response({'detail': 'you can\'t donate more cards for this donate object'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        donate_user = donate_obj.owner
        if donate_user.userClan != user.userClan:
            return Response({'detail': 'invalid request -> you are not in same clan'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if user is donate_user:
            return Response({'detail': 'you can\'t donate for yourself :D'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        donator_card = Card.objects.filter(cardType=donate_obj.cardType).filter(user=user)
        if donator_card.count() > 1:
            return Response({'detail': 'invalid request -> you have more than one card from this type'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if donator_card.count() == 0:
            return Response({'detail': 'invalid request -> you don\'t have any card from this type'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        donator_card = donator_card[0]
        if donator_card.cardCount < 1:
            return Response({'detail': 'invalid request -> you don\'t enough card to donate'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        destination_card = Card.objects.filter(cardType=donate_obj.cardType).filter(user=donate_user)[0]
        donator_card.cardCount -= 1
        destination_card.cardCount += 1
        destination_card.save()
        donator_card.save()

        earned_xp, earned_gold = DonationConf.donate_reward(donate_obj.cardType.cardRarity)

        gold_data = user.add_gold(earned_gold)
        xp_data = user.add_xp(earned_xp)
        user.clanData.donate_count += 1
        user.clanData.daily_donate_count += 1
        user.clanData.save()
        user.save()

        if user_donate_count is None:
            donate_obj.donators[str(user.idUser)] = '1'
        else:
            donate_obj.donators[str(user.idUser)] = str(int(user_donate_count) + 1)

        donate_obj.donatedCardCount += 1
        donate_obj.save()

        # TODO: do something after donation object done
        # if donate_obj.donatedCardCount == donate_obj.requiredCardCount:
        #     print('done')

        data = serializer.DonationSerializer(donate_obj).data
        return Response({'donate_data': data, 'xp_data': xp_data, 'gold_data': gold_data},
                        status=status.HTTP_201_CREATED)


class ClanDetail(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def get(request, pk):
        clan = Clan.get_object(pk)
        clan = serializer.ClanProfileSerializer(clan)
        return Response(clan.data, status=status.HTTP_202_ACCEPTED)


class MyClanDetail(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def get(request):
        user = request.user.user
        clan = user.userClan
        clan = serializer.ClanSerializer(clan)
        return Response(clan.data, status=status.HTTP_202_ACCEPTED)


class ClanMember(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request, clan_pk, action):
        if action == "join":
            user = request.user.user
            clan = Clan.get_object(pk=clan_pk)
            user.userClan = clan
            # TODO: update score and other things
            if user.clanData is None:
                clan_data = UserClanData.objects.create()
                user.clanData = clan_data
            user.save()

            user_id = user.backtory_userId
            connectivity_id = '575ea689e4b0e357ac17fd31'
            url = "https://ws.backtory.com/connectivity/chat/group/addMember"
            # TODO : auth token master from cache
            auth = "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpudWxsLCJpc19ndWVzdCI6ZmFsc2UsInNjb3BlIjpbIm1hc3RlciJdLCJleHAiOjE0NzE2NzU4MDEsImp0aSI6IjUzODc1MzEyLTY1MDktNDI3ZC04ZmRmLTEyODJkOTUyOTJmNiIsImNsaWVudF9pZCI6IjU3NGQ5YTg0ZTRiMDMzNzI0Njg5OTdmOCJ9.EtvXGKJ3AUesisjMKkJrgHKFFrbLL7ZYalg6TGVVvb4sFujq_xwt1aypkws25xm6ojZj1A7EUKfk1RjHIz-yXyI_w5_S3rrfo94EuRhXTtbhiEPlUr5ppxVXGXkhjchD22aB2fV9UASkxG21-kKuQmCkj8DyXVCrilBDNTqGg1sDq5xlvZukl7-yup7CV2AUBqNaLaowMS0OHtUoKusMTyzZ_Cn6OxYCKMfd4t9yg90tzhKN38sL6ynYp8tKcxYk25MwgM7q9i7cY8xFItczn9NSUzupr-ks_3gcBu6WegERyVUln1qRTejG0XJ6BArBxT8KGHQEg-VrFas6E_F3QA"
            headers = {
                'Authorization': auth,
                'X-Backtory-Connectivity-Id': connectivity_id,
                "X-Backtory-User-Id": clan.backtory_group_owner,
                "Content-Type": "application/json"
            }
            data = {
                "groupId": clan.backtory_group_id,
                "userId": user_id,
            }
            r1 = requests.post(url, json=data, headers=headers)
            print(r1.json())
            if r1.status_code != 201:
                print('group not registered on backtory')
                #TODO: log and do it again :D

            clan = serializer.ClanSerializer(clan)
            return Response(clan.data, status=status.HTTP_201_CREATED)
        if action == "leave":
            user = request.user.user
            clan = Clan.get_object(pk=clan_pk)
            if user.userClan == clan:
                user.userClan = None
                # TODO: update score and other things
                user.clanData.donate_count = 0
                user.clanData.lastRequestTime = 0
                user.clanData.position = 0
                user.clanData.save()
                user.save()
                user_id = user.backtory_userId
                connectivity_id = '575ea689e4b0e357ac17fd31'
                url = "https://ws.backtory.com/connectivity/chat/group/removeMember"
                # TODO : auth token master from cache
                auth = "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpudWxsLCJpc19ndWVzdCI6ZmFsc2UsInNjb3BlIjpbIm1hc3RlciJdLCJleHAiOjE0NzE2NzU4MDEsImp0aSI6IjUzODc1MzEyLTY1MDktNDI3ZC04ZmRmLTEyODJkOTUyOTJmNiIsImNsaWVudF9pZCI6IjU3NGQ5YTg0ZTRiMDMzNzI0Njg5OTdmOCJ9.EtvXGKJ3AUesisjMKkJrgHKFFrbLL7ZYalg6TGVVvb4sFujq_xwt1aypkws25xm6ojZj1A7EUKfk1RjHIz-yXyI_w5_S3rrfo94EuRhXTtbhiEPlUr5ppxVXGXkhjchD22aB2fV9UASkxG21-kKuQmCkj8DyXVCrilBDNTqGg1sDq5xlvZukl7-yup7CV2AUBqNaLaowMS0OHtUoKusMTyzZ_Cn6OxYCKMfd4t9yg90tzhKN38sL6ynYp8tKcxYk25MwgM7q9i7cY8xFItczn9NSUzupr-ks_3gcBu6WegERyVUln1qRTejG0XJ6BArBxT8KGHQEg-VrFas6E_F3QA"
                headers = {
                    'Authorization': auth,
                    'X-Backtory-Connectivity-Id': connectivity_id,
                    "X-Backtory-User-Id": clan.backtory_group_owner,
                    "Content-Type": "application/json"
                }
                data = {
                    "groupId": clan.backtory_group_id,
                    "userId": user_id,
                }
                r1 = requests.post(url, json=data, headers=headers)
                if r1.status_code != 201:
                    print('group not registered on backtory')
                    #TODO: log and do it again :D

                return Response({}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': "you are not member of this clan"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': "invalid action"}, status=status.HTTP_400_BAD_REQUEST)


class ClanList(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request):
        user = request.user.user
        if user.gold < 1000:
            return Response({'detail': 'not enough gold.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if user.level < 3:
            return Response({'detail': 'clans unlock at level 3.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        clan = serializer.ClanSerializer(data=request.data)
        if clan.is_valid():
            clan_obj = clan.save()
            if user.clanData is None:
                clan_data = UserClanData.objects.create()
                user.clanData = clan_data
            user.clanData.position = 3
            user.clanData.save()
            user.userClan = clan_obj
            # TODO: get required gold dynamic from function
            gold_data = user.add_gold(-1000)
            user_id = user.backtory_userId
            connectivity_id = '575ea689e4b0e357ac17fd31'
            url = "https://ws.backtory.com/connectivity/chat/group/create"
            # TODO : auth token master from cache
            auth = "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpudWxsLCJpc19ndWVzdCI6ZmFsc2UsInNjb3BlIjpbIm1hc3RlciJdLCJleHAiOjE0NzE2NzU4MDEsImp0aSI6IjUzODc1MzEyLTY1MDktNDI3ZC04ZmRmLTEyODJkOTUyOTJmNiIsImNsaWVudF9pZCI6IjU3NGQ5YTg0ZTRiMDMzNzI0Njg5OTdmOCJ9.EtvXGKJ3AUesisjMKkJrgHKFFrbLL7ZYalg6TGVVvb4sFujq_xwt1aypkws25xm6ojZj1A7EUKfk1RjHIz-yXyI_w5_S3rrfo94EuRhXTtbhiEPlUr5ppxVXGXkhjchD22aB2fV9UASkxG21-kKuQmCkj8DyXVCrilBDNTqGg1sDq5xlvZukl7-yup7CV2AUBqNaLaowMS0OHtUoKusMTyzZ_Cn6OxYCKMfd4t9yg90tzhKN38sL6ynYp8tKcxYk25MwgM7q9i7cY8xFItczn9NSUzupr-ks_3gcBu6WegERyVUln1qRTejG0XJ6BArBxT8KGHQEg-VrFas6E_F3QA"
            headers = {
                'Authorization': auth,
                'X-Backtory-Connectivity-Id': connectivity_id,
                "X-Backtory-User-Id": user_id,
                "Content-Type": "application/json"
            }
            data = {
                "name": clan_obj.clanName,
                "type": "Public",
            }
            r1 = requests.post(url, json=data, headers=headers)
            if r1.status_code != 201:
                print('group not registered on backtory')
                #TODO: log and do it again :D
            group_id = r1.json()['groupId']
            clan_obj.backtory_group_id = group_id
            clan_obj.backtory_group_owner = user_id
            clan_obj.save()
            return Response({'clan_data': clan.data, 'gold_data': gold_data}, status=status.HTTP_201_CREATED)
        return Response(clan.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class SearchClanByName(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def get(request, query):
        # clans = Clan.objects.filter(Q(clanName__icontains=query) | Q(clanDescription__icontains=query) )[:20]
        clans = Clan.objects.filter(clanName__icontains=query)[:20]
        data = list()
        for clan in clans:
            data.append(serializer.ClanMinimalSerializer(clan).data)
        return Response({'results': data}, status=status.HTTP_200_OK)


class DonateRequest(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request):
        user = request.user.user
        last_req = user.clanData.lastRequestTime
        passed_time = int(time.time()) - last_req

        remain_time = DonationConf.donate_request_period() - passed_time
        if remain_time > 0:
            return Response({"detail": "{0} seconds remain for next request".format(remain_time)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        print(request.data)
        card_type_id = request.data["card_type_id"]
        card_type = CardType.objects.get(Cardid=card_type_id)
        donate_obj = Donation()
        donate_obj.owner = user
        donate_obj.cardType = card_type
        donate_obj.clan = user.userClan
        donate_obj.requiredCardCount = DonationConf.donate_request_capacity(user.leagueLevel, card_type_id)
        donate_obj.donators = {}
        donate_obj.save()

        user.clanData.lastRequestTime = donate_obj.startTime
        user.clanData.save()

        data = serializer.DonationSerializer(donate_obj).data
        return Response(data, status=status.HTTP_201_CREATED)


class PromoteUser(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request):
        user = request.user.user
        data = request.data
        promoted_user_id = int(data['userID'])
        user_clan_data = user.clanData
        promoted_user = User.get_object(pk=promoted_user_id)
        if user_clan_data.position < 2:
            return Response({'detail': 'your position in clan < co-leader'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif user_clan_data.position is 2:
            if promoted_user.clanData.position >= 2:
                return Response({'detail': 'can not promote to leader'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            promoted_user.clanData.position += 1
        elif user_clan_data.position is 3:
            if promoted_user.clanData.position >= 2:
                return Response({'detail': 'can not promote to leader'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            promoted_user.clanData.position += 1
        promoted_user.clanData.save()
        response_data = {
            'userID': promoted_user_id,
            'new_position': promoted_user.clanData.position
        }
        return Response(response_data, status=status.HTTP_200_OK)


class DemoteUser(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request):
        user = request.user.user
        data = request.data
        demoted_user_id = int(data['userID'])
        user_clan_data = user.clanData
        demoted_user = User.get_object(pk=demoted_user_id)
        if user_clan_data.position < 2:
            return Response({'detail': 'your position in clan < co-leader'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif user_clan_data.position is 2:
            if demoted_user.clanData.position != 1:
                return Response({'detail': 'can not demote co leader and leader'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            demoted_user.clanData.position -= 1
        elif user_clan_data.position is 3:
            if demoted_user.clanData.position == 3 or demoted_user.clanData.position == 0:
                return Response({'detail': 'can not demote leader in this way'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            demoted_user.clanData.position -= 1
        demoted_user.clanData.save()
        response_data = {
            'userID': demoted_user_id,
            'new_position': demoted_user.clanData.position
        }
        return Response(response_data, status=status.HTTP_200_OK)


class AcceptUser(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request):
        user = request.user.user
        clan = user.userClan
        data = request.data
        accepted_user_id = data['accepted_user_id']
        waiting_list = dict(clan.waiting_list)
        if user.clanData.position == 0:
            return Response({'detail': 'member user can not accept users'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if accepted_user_id in waiting_list:
            del waiting_list[accepted_user_id]
            clan.waiting_list = waiting_list
            clan.save()
            accepted_user = User.get_object(pk=int(accepted_user_id))
            accepted_user.userClan = clan
            if accepted_user.clanData is None:
                clan_data = UserClanData.objects.create()
                accepted_user.clanData = clan_data
            accepted_user.clanData.position = 0
            accepted_user.clanData.donate_count = 0
            accepted_user.clanData.lastRequestTime = -1
            accepted_user.clanData.save()
            user_clan_info = serializer.ClanUserSerializer(accepted_user).data
            return Response({'accepted_user': user_clan_info}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'accepted user does not exist in waiting list'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class DeclineUser(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request):
        user = request.user.user
        clan = user.userClan
        data = request.data
        declined_user_id =data['declined_user_id']
        waiting_list = dict(clan.waiting_list)
        if user.clanData.position != 3:
            return Response({'detail': 'can not decline user request'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if declined_user_id in waiting_list:
            del waiting_list[declined_user_id]
            clan.waiting_list = waiting_list
            clan.save()
        else:
            return Response({'detail': 'declined user does not exist in waiting list'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class KickMember(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request):
        user = request.user.user
        data = request.data
        kicked_user_id =data['kicked_user_id']
        kicked_user = User.get_object(pk=kicked_user_id)
        if user.clanData.position <= kicked_user.clanData.position:
            return Response({"detail": "can not kick this position"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            kicked_user.userClan = None
            # TODO: update score and other things
            kicked_user.clanData.donate_count = 0
            kicked_user.clanData.lastRequestTime = 0
            kicked_user.clanData.position = 0
            kicked_user.clanData.save()
            kicked_user.save()
            return Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)


class InviteUser(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request):
        user = request.user.user
        clan = user.userClan
        data = request.data
        if user.clanData.position == 0:
            return Response({"detail": "this position can not invite user"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        invite_user_id = data['invite_user_id']
        invite_user = User.get_object(pk=invite_user_id)
        data = {'time': int(time.time()), 'clan_name': clan.clanName}
        invite_user.invitaion_list[str(clan.idClan)] = json.dumps(data)
        invite_user.save()
        return Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)


class AcceptUser(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @staticmethod
    def post(request):
        user = request.user.user
        data = request.data
        accepted_clan_id = data['accepted_clan_id']
        invitation_list = dict(user.invitaion_list)
        if accepted_clan_id in invitation_list:
            clan = Clan.get_object(pk=accepted_clan_id)
            del invitation_list[accepted_clan_id]
            user.invitaion_list = invitation_list
            user.userClan = clan
            if user.clanData is None:
                clan_data = UserClanData.objects.create()
                user.clanData = clan_data
            user.clanData.position = 0
            user.clanData.donate_count = 0
            user.clanData.lastRequestTime = -1
            user.clanData.save()
            clan_info = serializer.ClanSerializer(clan).data
            return Response({'accepted_user': clan_info}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'accepted clan does not exist in invitation list'}, status=status.HTTP_406_NOT_ACCEPTABLE)

