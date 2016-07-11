from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.http import JsonResponse, Http404
from django.db import IntegrityError

from django.contrib.auth.models import User as djangoUser
from django.contrib.auth import authenticate, login

from django.core.exceptions import ObjectDoesNotExist

from app1 import serializers as serializer
from app1.models import User, Card, CardType, Clan, UserClanData, RewardPack

import reward_conf
import app1.card_conf as cardConf
from leaderboard.leaderboard import Leaderboard



from datetime import datetime
from random import *
import uuid
import time
import hashlib
import json
import math


@api_view(['POST', 'GET'])
def deck(request):

    if request.method == 'GET':
        data = request.GET
        userID = data['userID']
        try:
            user = User.objects.get(idUser=userID)
            deck_order = {'deck_order': user.deck1}
            return JsonResponse(deck_order, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response('user not found', status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        data = request.POST
        userID = num(data['userID'])
        deck_str = data['deck']
        deck_order = json.loads(deck_str)
        try:
            #TODO: check for validity of deck numbers!
            user = User.objects.get(idUser=userID)
            user.deck1 = deck_order
            user.save()
            return JsonResponse({}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return JsonResponse({'error':'user not found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def bot_deck(request):
    a = {'deck_order': random.choice([
        [15, 3, 5, 7, 9, 2, 16, 12],
        [6, 17, 8, 1, 11, 14, 16, 18],
        [12, 17, 15, 5, 19, 13, 6, 14]
    ])}
    return JsonResponse(a, status=status.HTTP_200_OK)

    
# @api_view(['GET'])
# def card(request):
#
#     if request.method == 'GET':
#         data = request.GET
#         userID = num(data['userID'])
#         cards = Card.objects.filter(user=userID)
#         if len(cards) < 1:
#             return Response('no card!', status=status.HTTP_400_BAD_REQUEST)
#         card_list = []
#         for card_element in cards:
#             card_list.append(card_element.cardType.Cardid)
#         responseData = {
#             'userID': userID,
#             'cardList': json.dumps(card_list, separators=(',', ':'))
#         }
#         return JsonResponse(responseData, status=status.HTTP_200_OK)





def calculate_upgrade_cost(level, count):

    return (10,10)

@api_view(['POST'])
def match_request(request):
    if request.method == 'POST':
        data = request.POST
        userID = data['userID']
        deviceID = data['deviceID']
        # retrieve user data from db
        now = datetime.now().__str__()
        # file = open('private.pem', 'r')
        # sk = RSA.importKey(file.read())
        # file.close()
        # signer = PKCS1_v1_5.new(sk)
        # msg = userID + deviceID + now
        # h = SHA256.new(msg.encode())
        # signature = signer.sign(h)
        # signb64 = b64encode(signature).decode()
        signb64 = ''
        responseData = {
                'userID': userID,
                'deviceID': deviceID,
                'time': now,
                'serverIP': 'sl.hexino.ir',
                'port': '16160',
                'signature': signb64
            }
        return JsonResponse(responseData, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_username(request):

    if request.method == 'POST':
        data = request.POST
        userID = (data.get('userID', default=None))
        username = data.get('username', default=None)
        user = None

        if userID is not None:
            user = User.objects.get(idUser=userID)

        user.username = username
        user.save()
        highscore_lb = Leaderboard('Bazuka_V1')
        highscore_lb.rank_member(user.username, user.trophiesCount, user.idUser)

        responseData = {
            'userID': userID,
            'deviceID': user.deviceID,
            'username': username
        }
        return JsonResponse(responseData, status=status.HTTP_200_OK)


@api_view(['POST'])
def bug_report(request):
    if request.method == 'POST':
        data = request.POST
        userID = data.get('userID', default=None)
        deviceID = data.get('deviceID', default=None)
        title = data.get('title', default=None)
        text = data.get('text', default=None)
        now = datetime.now().__str__()

        user = None
        if deviceID is not None:
            user = User.objects.get(deviceID=deviceID)
        if user is None:
            return Response('invalid ', status=status.HTTP_400_BAD_REQUEST)
        if str(user.idUser) != userID:
            return Response('invalid ', status=status.HTTP_400_BAD_REQUEST)
        file = open('/home/soheil/hexino.ir/Bazuka_General_Server/bug_report/user_'+userID+'_time_'+now, 'wt+')
        file.write(title+'\n'+text)
        file.close()
        return JsonResponse({}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_updates(request):

    if request.method == 'GET':
        data = request.GET
        deviceID = data.get('deviceID', default=None)
        userID = (data.get('userID', default=None))
        user = None
        created = None
        if userID is None:
            user, created = User.objects.get_or_create(deviceID=deviceID)
        else:
            user = User.objects.get(idUser=userID)
#        if created:
#            highscore_lb = Leaderboard('Bazuka_V1')
#            highscore_lb.rank_member(user.username, user.trophy, user.idUser)
        userID = user.idUser
        username = user.username

        card_list = []
        for card_element in user.cards.all():
            card_list.append(card_element.cardType.Cardid)
        responseData = {
            'userID': userID,
            'username': username,
            'deviceID': deviceID,
            'cardList': card_list,
            'deck1': user.deck1,
            'trophy': 0,
            'version':"1.1.0"
        }
        return JsonResponse(responseData, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_match_result(request):
    if request.method == 'POST':
        data = request.POST
        user1ID = data.get('user1ID', default=None)
        user2ID = data.get('user2ID', default=None)
        roomID = data.get('roomID', default=None)
        user1Score = data.get('user1Score', default=None)
        user2Score = data.get('user2Score', default=None)
        scoreDiff = abs(int(user1Score) - int(user2Score))
        if user1ID is None or user2ID is None:
            return Response('invalid userID', status=status.HTTP_400_BAD_REQUEST)
        userID = [user1ID, user2ID]
        winner = data.get('winner', default=None)
        turn = data.get('turn', default=None)
        u1diff = None
        u2diff = None
        if winner is None or turn is None :
            return Response('invalid userID', status=status.HTTP_400_BAD_REQUEST)

        if int(user2ID) == -2 :
            user = User.objects.get(idUser=user1ID)
            if user.winCount != 0 or user.loseCount != 0:
                responseData = {
                    'user1': {
                        'userID': user.idUser,
                        'trophy_sum': user.trophiesCount,
                        'trophy_diff': 0
                    },
                    'user2': {
                        'userID': -1,
                        'trophy_sum': 0,
                        'trophy_diff': 0
                    },
                    'winner': int(winner),
                    'roomID': roomID
                }   
                return JsonResponse(responseData, status=status.HTTP_200_OK)
            else:    
                udiff = None
                if int(user1Score) > int(user2Score):
                    user.winCount += 1
                    udiff = calculate_trophy(user.trophiesCount, user.level, True, int(turn), scoreDiff)
                    user.trophiesCount += udiff
                else:
                    user.loseCount += 1
                    udiff = calculate_trophy(user.trophiesCount, user.level, False, int(turn), scoreDiff)
                    user.trophiesCount += udiff
                user.save()
                highscore_lb = Leaderboard('Bazuka_V1')
                highscore_lb.rank_member(user.username, user.trophiesCount, user.idUser)
                responseData = {
                    'user1': {
                        'userID': user.idUser,
                        'trophy_sum': user.trophiesCount,
                        'trophy_diff': udiff
                    },
                    'user2': {
                        'userID': -1,
                        'trophy_sum': 0,
                        'trophy_diff': 0
                    },
                    'winner': int(winner),
                    'roomID': roomID
                }   
                return JsonResponse(responseData, status=status.HTTP_200_OK)
        elif int(user2ID) == -1 :
            user = User.objects.get(idUser=user1ID)
            udiff = None
            if int(user1Score) > int(user2Score):
                user.winCount += 1
                udiff = calculate_trophy(user.trophiesCount, user.level, True, int(turn), scoreDiff)
                user.trophiesCount += udiff
            else:
                user.loseCount += 1
                udiff = calculate_trophy(user.trophiesCount, user.level, False, int(turn), scoreDiff)
                user.trophiesCount += udiff
            user.save()
            highscore_lb = Leaderboard('Bazuka_V1')
            highscore_lb.rank_member(user.username, user.trophiesCount, user.idUser)
            responseData = {
                'user1': {
                    'userID': user.idUser,
                    'trophy_sum': user.trophiesCount,
                    'trophy_diff': udiff
                },
                'user2': {
                    'userID': -1,
                    'trophy_sum': 0,
                    'trophy_diff': 0
                },
                'winner': int(winner),
                'roomID': roomID
            }   
            return JsonResponse(responseData, status=status.HTTP_200_OK)
        else:
            user1 = User.objects.get(idUser=userID[int(winner)])
            user2 = User.objects.get(idUser=userID[1 - int(winner)])
            if int(user1Score) == -1 or int(user2Score) == -1:
                user1.winCount += 1
                u1diff = 20
                user1.trophiesCount += u1diff
        
                user2.loseCount += 1
                u2diff = -10
                if user2.trophiesCount < 10:
                    u2diff = -user2.trophiesCount
                user2.trophiesCount += u2diff
                
            else:
                user1.winCount += 1
                u1diff = calculate_trophy(user1.trophiesCount, user1.level, True, int(turn), scoreDiff)
                user1.trophiesCount += u1diff
        
                user2.loseCount += 1
                u2diff = calculate_trophy(user2.trophiesCount, user2.level, False, int(turn), scoreDiff)
                user2.trophiesCount += u2diff
    
            user1.save()
            user2.save()
            highscore_lb = Leaderboard('Bazuka_V1')
            highscore_lb.rank_member(user1.username, user1.trophiesCount, user1.idUser)
            highscore_lb.rank_member(user2.username, user2.trophiesCount, user2.idUser)

            responseData = {
                'user1': {
                    'userID': user1.idUser,
                    'trophy_sum': user1.trophiesCount,
                    'trophy_diff': u1diff
                },
                'user2': {
                    'userID': user2.idUser,
                    'trophy_sum': user2.trophiesCount,
                    'trophy_diff': u2diff
                },
                'winner': 0,
                'roomID': roomID
    
            }
            return JsonResponse(responseData, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_leaders(request):
    if request.method == 'GET':
        # data = request.data
        # userID = data['userID']
        # deviceID = data['deviceID']
        highscore_lb = Leaderboard('Bazuka_V1')
        top_100 = highscore_lb.top(100)
        responseData = {
            "top": top_100
        }
        return JsonResponse(responseData, status=status.HTTP_200_OK,encoder=MyEncoder)

def calculate_trophy(user1_trophy, user2_trophy):
    """
    user1 is game winner
    :param user1_trophy:
    :param user2_trophy:
    :return:
    """
    earned = 30 + max(min(math.ceil((user1_trophy - user2_trophy)/100), 10), -10)
    if user2_trophy < earned:
        return 30, user2_trophy
    else:
        return earned, earned

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
          return obj.decode()
        return json.JSONEncoder.default(self, obj)


class ClanMember(APIView):
    def post(self, request, clan_pk, action, format=None):
        print(action)
        print(type(clan_pk))
        print(type(action))
        if action == "join":
            uid = request.data['userid']
            user = UserDetail.get_object(self=None, pk=uid)
            clan = ClanDetail.get_object(self=None, pk=clan_pk)
            user.userClan = clan
            #TODO: update score and other things
            if user.clanData is None:
                clanData = UserClanData.objects.create()
                user.clanData = clanData
            user.save()
            clan = serializer.ClanSerializer(clan)
            return Response(clan.data, status=status.HTTP_201_CREATED)
        if action == "leave":
            uid = request.data['userid']
            user = UserDetail.get_object(self=None, pk=uid)
            clan = ClanDetail.get_object(self=None, pk=clan_pk)
            if uid != str(user.userClan):
                user.userClan = None
                #TODO: update score and other things
                user.clanData.donate_count = 0
                user.clanData.lastRequestTime = 0
                user.clanData.position = 0
                user.clanData.save()
                user.save()
                clan = serializer.ClanSerializer(clan)
                return Response(clan.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': "clanLeader can not leave the clan"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': "invalid action"}, status=status.HTTP_400_BAD_REQUEST)




class UserList(APIView):
    #TODO: verify real client
    def post(self, request, Format=None):
        """
        register new user
        :param request:
        :param Format:
        :return: uuid and password for new user in json format
        """
        username = uuid.uuid4().hex[:29]
        password = 'id_' + username + 'time_{0}'.format(int(time.time() * 100))
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        password = m.hexdigest()
        user = self.create_basic_user(username, password)
        user = User.objects.create(basicUser=user)
        return Response({"uuid": username, "password": password}, status=status.HTTP_201_CREATED)

    def create_basic_user(self, username, password):
        try:
            user = djangoUser.objects.create_user(username, email=None, password=password)
            return user
        except IntegrityError:
            print('here')
            username = uuid.uuid4().hex[:29]
            return self.create_basic_user(username, password)





class UserDetail(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user = serializer.UserSerializer(user)
        return Response(user.data, status=status.HTTP_200_OK)

class ClanList(APIView):
    def post(self, request, format=None):
        clan = serializer.ClanSerializer(data=request.data)
        if clan.is_valid():
            clanobj = clan.save()#TODO: set clan creator to user --> auth
            uid = request.data['userid']
            user = UserDetail.get_object(self=None, pk=uid)
            if user.clanData is None:
                clanData = UserClanData.objects.create()
                user.clanData = clanData
            user.clanData.position = 1
            user.clanData.save()
            user.userClan = clanobj
            user.save()
            return Response(clan.data, status=status.HTTP_201_CREATED)
        return Response(clan.errors, status=status.HTTP_400_BAD_REQUEST)

class ClanDetail(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Clan.objects.get(pk=pk)
        except Clan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        clan = self.get_object(pk)
        clan = serializer.ClanSerializer(clan)
        return Response(clan.data)



class CardUpgrade(APIView):
    def post(self, request, cardID, Format=None):
        user = request.user.user
        if not user.is_authenticated():
            return Response({'detail': 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
        cards = Card.objects.filter(user=user.idUser).filter(cardType=cardID)
        if len(cards) != 1:
            return Response({'detail': 'card/user not found'}, status=status.HTTP_400_BAD_REQUEST)

        card = cards[0]

        required_gold = cardConf.CardUpgrade.required_golds(card.cardLevel, card.cardType.cardRarity)
        required_cards = cardConf.CardUpgrade.required_cards(card.cardLevel)
        xp = cardConf.CardUpgrade.earned_xp(card.cardLevel, card.cardType.cardRarity)

        if required_cards > card.cardCount:
            return Response({'detail': 'not enough cards'}, status=status.HTTP_400_BAD_REQUEST)
        if required_gold > user.gold:
            return Response({'detail': 'not enough golds'}, status=status.HTTP_400_BAD_REQUEST)
        card.cardLevel += 1
        card.cardCount -= required_cards
        user.gold -= required_gold
        user.xp += xp
        user.save()
        card.save()
        response_data = {'userID': user.idUser, 'cardTypeID': cardID, 'cardLevel': card.cardLevel,
                         'cardCount': card.cardCount, 'excess_xp': xp, 'upgrade_gold_cost': required_gold,
                         'next_gold': cardConf.CardUpgrade.required_golds(card.cardLevel, card.cardType.cardRarity),
                         'next_card_count': cardConf.CardUpgrade.required_cards(card.cardLevel)
                         }
        return Response(response_data, status=status.HTTP_200_OK)


class SetUsername(APIView):

    def post(self, requset, Format=None):
        if not requset.user.is_authenticated():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        username = requset.data['username']
        user = requset.user.user
        user.username = username
        user.save()
        user = serializer.UserSerializer(user)
        return Response(user.data, status=status.HTTP_200_OK)


class Me(APIView):

    def get(self, request, Format=None):
        if request.user.is_authenticated():
            my_user = request.user.user
            user = serializer.UserSerializer(my_user)
            return Response(user.data, status=status.HTTP_200_OK)
        else :
            return  Response({},status=status.HTTP_401_UNAUTHORIZED)


class ClanMembership(APIView):

    def post(self, request, clan_pk, action, format=None):
        if not request.user.is_authenticated():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        print(action)
        print(type(clan_pk))
        print(type(action))
        if action == "join":
            user = request.user.user
            clan = ClanDetail.get_object(self=None, pk=clan_pk)
            user.userClan = clan
            #TODO: update score and other things
            if user.clanData is None:
                clanData = UserClanData.objects.create()
                user.clanData = clanData
            user.save()
            clan = serializer.ClanSerializer(clan)
            return Response(clan.data, status=status.HTTP_201_CREATED)
        if action == "leave":
            user = request.user.user
            clan = ClanDetail.get_object(self=None, pk=clan_pk)
            if user.idUser != str(user.userClan):
                user.userClan = None
                #TODO: update score and other things
                user.clanData.donate_count = 0
                user.clanData.lastRequestTime = 0
                user.clanData.position = 0
                user.clanData.save()
                user.save()
                clan = serializer.ClanSerializer(clan)
                return Response(clan.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': "clanLeader can not leave the clan"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': "invalid action"}, status=status.HTTP_400_BAD_REQUEST)


class Deck(APIView):

    def get(self, request, Format=None):
        user = request.user.user
        if user.is_authenticated():
            deck_order = {'deck_order': user.deck1}
            return Response(deck_order, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, Format=None):
        user = request.user.user
        if user.is_authenticated():
            deck_str = request.data['deck']
            deck_order = json.loads(deck_str)
            user.deck1 = deck_order
            user.save()
            return Response({}, status=status.HTTP_206_PARTIAL_CONTENT)#TODO: response
        else:
            return Response({'detail': 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)


class MatchResult(APIView):
    def post(self, request, matchid=None, Format=None):
        data = request.data
        try:
            user1 = {
                'type': data['user1_type'],
                'score': data['user1_score'],
                'userID': data['user1_userID']
            }
            user2 = {
                'type': data['user2_type'],
                'score': data['user2_score'],
                'userID': data['user2_scoreID']
            }
            match_info = {
                'winner': data['match_info_winner'],
                'roomID': data['match_info_roomID'],
                'turn': data['match_info_turn']
            }
        except KeyError:
            return Response({'detail': 'incomplete info'}, status=status.HTTP_400_BAD_REQUEST)

        if user2['type'] is 'tutorial':
            responseData = self.match_result_tutorial(user1, user2, match_info)
        elif user2['type'] is 'bot':
            responseData = self.match_result_bot(user1, user2, match_info)
        elif user2['type'] is 'player':
            responseData = self.match_result(user1, user2, match_info)

    def match_result_tutorial(self, user1, user2, match_info):
        user = User.objects.get(idUser=user1['userID'])
        if user.winCount != 0 or user.loseCount != 0:
            responseData = {
                'user1': {
                    'userID': user.idUser,
                    'trophy_sum': user.trophiesCount,
                    'trophy_diff': 0
                },
                'user2': {
                    'userID': -1,
                    'trophy_sum': 0,
                    'trophy_diff': 0
                },
                'winner': int(match_info['winner']),
                'roomID': match_info['roomID']
            }
            return responseData
        else:
            scoreDiff = user1['score'] - user2['score']
            if scoreDiff > 0:
                user.winCount += 1
                udiff = 30
                user.trophiesCount += udiff
            else:
                user.loseCount += 1
                udiff = 0
                user.trophiesCount += udiff
            user.save()
            highscore_lb = Leaderboard('Bazuka_V1')
            highscore_lb.rank_member(user.username, user.trophiesCount, user.idUser)
            responseData = {
                'user1': {
                    'userID': user.idUser,
                    'trophy_sum': user.trophiesCount,
                    'trophy_diff': udiff
                },
                'user2': {
                    'userID': -1,
                    'trophy_sum': 0,
                    'trophy_diff': 0
                },
                'winner': int(match_info['winner']),
                'roomID': match_info['roomID']
            }
            return responseData

    def match_result_bot(self, user1, user2, match_info):

            user1_obj = User.objects.get(idUser=user1['userID'])
            scoreDiff = int(user1['score']) - int(user2['score'])
            if scoreDiff > 0:
                user1_obj.winCount += 1
                udiff = 30
                user1_obj.trophiesCount += udiff
            else:
                user1_obj.loseCount += 1
                udiff = 30
                user1_obj.trophiesCount -= udiff
            user1_obj.save()
            highscore_lb = Leaderboard('Bazuka_V1')
            highscore_lb.rank_member(user1_obj.username, user1_obj.trophiesCount, user1_obj.idUser)
            responseData = {
                'user1': {
                    'userID': user1_obj.idUser,
                    'trophy_sum': user1_obj.trophiesCount,
                    'trophy_diff': udiff
                },
                'user2': {
                    'userID': -1,
                    'trophy_sum': 0,
                    'trophy_diff': 0
                },
                'winner': int(match_info['winner']),
                'roomID': match_info['roomID']
            }
            return responseData

    def match_result(self, user1, user2, match_info):
        userID = [user1['userID'], user2['userID']]
        winner = int(match_info['winner'])
        user1_obj = User.objects.get(idUser=userID[winner])
        user2_obj = User.objects.get(idUser=userID[1 - winner])

        if int(user1['score']) == -1 or int(user2['score']) == -1:#TODO: someone left the match
            user1_obj.winCount += 1
            u1diff = 20
            user1_obj.trophiesCount += u1diff

            user2_obj.loseCount += 1
            u2diff = -10
            if user2_obj.trophiesCount < 10:
                u2diff = -user2_obj.trophiesCount
            user2_obj.trophiesCount += u2diff
        else:
            u1diff, u2diff = calculate_trophy(user1_obj.trophiesCount, user2_obj.trophiesCount)
            user1_obj.winCount += 1
            u1_trophy_data = user1_obj.add_trophy(u1diff)
            user2_obj.loseCount += 1
            u2_trophy_data = user2_obj.add_trophy(u2diff)
        pack = user1_obj.get_random_pack()

        user1_obj.save()
        user2_obj.save()
        # highscore_lb = Leaderboard('Bazuka_V1')
        # highscore_lb.rank_member(user1_obj.username, user1_obj.trophiesCount, user1_obj.idUser)
        # highscore_lb.rank_member(user2_obj.username, user2_obj.trophiesCount, user2_obj.idUser)

        responseData = {
            'user1': {
                'userID': user1_obj.idUser,
                'trophy_data': u1_trophy_data,
                'pack_data': {
                    'pack_league_level': pack.packLeagueLevel,
                    'pack_type': pack.packType,
                    'pack_timer': pack.unlockStartTime,
                } if pack is not None else {}
            },
            'user2': {
                'userID': user2_obj.idUser,
                'trophy_sum': user2_obj.trophiesCount,
                'trophy_diff': -u2diff
            },
            'winner': 0,
            'roomID': match_info['roomID']

        }

        return responseData

def num(s):
    try:
        return int(s)
    except ValueError:
        return -1




class UnpackReward(APIView):
    def get_object(self, pk):
        try:
            return RewardPack.objects.get(pk=pk)
        except RewardPack.DoesNotExist:
            raise Http404

    def post(self, request, reward_pk, Format=None):
        user = request.user.user
        pack = self.get_object(reward_pk)
        if int(time.time()) - pack.unlockStartTime < reward_conf.pack_wait_time[pack.packType]:
            return Response({'detail': 'invalid unpack action'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_authenticated():
            return Response({'detail': 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

        gold, total_card = self.reward(pack.packType, pack.packLevel)
        user.gold += gold

        pack.delete()
        user.save()
        return Response({}, status=status.HTTP_200_CREATED)

    def reward(self, packType, level):
        gold = randrange(reward_conf.PackTotalCards[packType][level][1],
                         reward_conf.PackTotalCards[packType][level][2])
        total_card = reward_conf.PackTotalCards[packType][level][0]
        return gold, total_card

    def get_or_create_card(self, card_type, user_id):
        card_obj, created = Card.objects.get_or_create(user=user_id, cardType=card_type)
        return card_obj


# class UnlockPack(APIView):
#
#     def get_object(self, pk):
#         try:
#             return RewardPack.objects.get(pk=pk)
#         except RewardPack.DoesNotExist:
#             raise Http404
#
#     def post(self, request, reward_pk, Format=None):
#         userID = request.data['userID']
#         pack = self.get_object(reward_pk)
#         pack.unlockStartTime = int(time.time())
#         pack.save()
#         pack = PackSerializer(pack)
#         return Response(pack.data, status=status.HTTP_201_CREATED)
