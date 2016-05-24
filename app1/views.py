from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from app1.models import User,Card,CardType
import json
from random import *
# from Crypto.Signature import PKCS1_v1_5
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import RSA
# from base64 import b64decode,b64encode

from datetime import datetime
from leaderboard.leaderboard import Leaderboard
from django.core.exceptions import ObjectDoesNotExist
# import pickle


# @api_view(['POST'])
# def upgrade_card(request):

#     if request.method == 'GET':
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     elif request.method == 'POST':
#         data = request.data
#         userID = data['userID']
#         cardID = data['cardID']
#         cards = Card.objects.filter(user=userID).filter(cardType=cardID)
#         if len(cards) != 1:
#             return Response('card/user not found', status=status.HTTP_400_BAD_REQUEST)
#         card = cards[0]
#         upgradeCost = calculate_upgrade_cost(card.cardLevel,card.cardCount)
#         if upgradeCost > card.cardCount:
#             return Response('not enough cards', status=status.HTTP_400_BAD_REQUEST)
#         card.cardLevel += 1
#         card.cardCount -= upgradeCost
#         card.save()
#         responseData = json.dumps({'userID':userID, 'cardID':cardID, 'cardLevel': card.cardLevel, 'cardCount': card.cardCount})
#         return Response(responseData, status=status.HTTP_200_CREATED)


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
        userID = data['userID']
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
def card(request):

    if request.method == 'GET':
        data = request.GET
        userID = data['userID']
        cards = Card.objects.filter(user=userID)
        if len(cards) < 1:
            return Response('no card!', status=status.HTTP_400_BAD_REQUEST)
        card_list = []
        for card_element in cards:
            card_list.append(card_element.cardType.Cardid)
        responseData = {
            'userID': userID,
            'cardList': json.dumps(card_list, separators=(',', ':'))
        }
        return JsonResponse(responseData, status=status.HTTP_200_OK)





def calculate_upgrade_cost(level, count):

    return 10

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
        userID = data.get('userID', default=None)
        username = data.get('username', default=None)
        user = None

        if userID is not None:
            user = User.objects.get(idUser=userID)

        user.username = username
        user.save()

        responseData = {
            'userID': userID,
            'deviceID': user.idDevice,
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
            user = User.objects.get(idDevice=deviceID)
        if user is None:
            return Response('invalid ', status=status.HTTP_400_BAD_REQUEST)
        if user.idUser != userID:
            return Response('invalid ', status=status.HTTP_400_BAD_REQUEST)
        file = open('./bug_report/user_'+userID+'_time_'+now, 'wt+')
        file.write(title+'\n'+text)
        file.close()
        return JsonResponse('Thanks', status=status.HTTP_200_OK)


@api_view(['GET'])
def get_updates(request):

    if request.method == 'GET':
        data = request.GET
        deviceID = data.get('deviceID', default=None)
        userID = data.get('userID', default=None)
        user = None
        created = None
        if userID is None:
            user, created = User.objects.get_or_create(idDevice=deviceID)
        else:
            user = User.objects.get(idUser=userID)
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
            'trophy': user.trophy
        }
        return JsonResponse(responseData, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_match_result(request):
    if request.method == 'POST':
        data = request.POST
        user1ID = data.get('user1ID', default=None)
        user2ID = data.get('user2ID', default=None)
        roomID = data.get('roomID', default=None)
        if user1ID is None or user2ID is None:
            return Response('invalid userID', status=status.HTTP_400_BAD_REQUEST)
        userID = [user1ID, user2ID]
        winner = data.get('winner', default=None)
        turn = data.get('turn', default=None)
        if winner is None or turn is None :
            return Response('invalid userID', status=status.HTTP_400_BAD_REQUEST)

        # time = data['time']
        # signb64 = data['b64sign']

        # file = open('public.pem', 'r')
        # pk = RSA.importKey(file.read())
        # file.close()
        # verifier = PKCS1_v1_5.new(pk)
        # msg = json.dumps({
        #     'user1ID': userID[0],
        #     'user2ID': userID[1],
        #     'winner': winner,
        #     'time': time
        # }, sort_keys=True, separators=(',', ':'))
        #
        # h = SHA256.new(msg.encode())
        # print(msg.encode())
        # print(h.hexdigest())
        # print(b64decode(signb64))
        # if not verifier.verify(h, b64decode(signb64)):
        #     return Response('wrong signature', status=status.HTTP_400_BAD_REQUEST)

        user1 = User.objects.get(idUser=userID[int(winner)])
        user2 = User.objects.get(idUser=userID[1 - int(winner)])

        user1.winCount += 1
        u1diff = calculate_trophy(user1.trophy, user1.level, True, turn)
        user1.trophy += u1diff

        user2.loseCount += 1
        u2diff = calculate_trophy(user2.trophy, user2.level, False, turn)
        user2.trophy += u2diff

        user1.save()
        user2.save()
        highscore_lb = Leaderboard('Bazuka_V1')
        highscore_lb.delete_leaderboard()
        highscore_lb.rank_member(user1.username, user1.trophy, user1.idUser)
        highscore_lb.rank_member(user2.username, user2.trophy, user2.idUser)

        responseData = {
            'user1': {
                'userID': user1.idUser,
                'trophy_sum': user1.trophy,
                'trophy_diff': u1diff
            },
            'user2': {
                'userID': user2.idUser,
                'trophy_sum': user2.trophy,
                'trophy_diff': u2diff
            },
            'winner': winner,
            'roomID': roomID

        }
        return JsonResponse(responseData, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_leaders(request):
    if request.method == 'GET':
        # data = request.data
        # userID = data['userID']
        # deviceID = data['deviceID']
        highscore_lb = Leaderboard('TheTree')
        top_100 = highscore_lb.top(100)
        responseData = {
            "top": top_100
        }
        return JsonResponse(responseData, status=status.HTTP_200_OK,encoder=MyEncoder)


def calculate_trophy(user_trophy, user_level, is_winner, turn):
    if is_winner:
        if turn < 10:
            return randint(15, 20)
        elif 10 <= turn < 20:
            return randint(25, 30)
        elif 20 <= turn < 30:
            return randint(35, 40)
        else:
            return 40
    if user_trophy <= 15:
        return -user_trophy
    return -15


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, bytes):
          return obj.decode()
       return json.JSONEncoder.default(self, obj)
