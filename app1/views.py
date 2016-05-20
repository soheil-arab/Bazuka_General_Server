from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from app1.models import User,Card,CardType
import json

# from Crypto.Signature import PKCS1_v1_5
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import RSA
# from base64 import b64decode,b64encode

from datetime import datetime
from leaderboard.leaderboard import Leaderboard
from django.core.exceptions import ObjectDoesNotExist
import pickle


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
            print('object with '+userID+' does not exist')
            return Response('user not found', status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        print('salam')
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
            print('object with '+userID+' does not exist')
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
            'cardList': json.dumps(card_list,separators=(',', ':'))
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
                'serverIP': 'alpha.hexino.ir',
                'port': '16160',
                'signature': signb64
            }
        return JsonResponse(responseData, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_username(request):

    if request.method == 'POST':
        data = request.POST
        userID = data['userID']
        deviceID = data['deviceID']
        username = data['username']
        user, created = User.objects.get_or_create(idDevice=deviceID)

        if created:
            userID = user.idUser

        user.username = username
        user.save()

        responseData = {
            'userID': userID,
            'deviceID': deviceID,
            'username': username
        }
        return JsonResponse(responseData, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_updates(request):

    if request.method == 'GET':
        data = request.GET
        deviceID = data['deviceID']
        user, created = User.objects.get_or_create(idDevice=deviceID)
        userID = user.idUser
        username = user.username

        card_list = []
        for card_element in user.cards.all():
            card_list.append(card_element.cardType.Cardid)
        responseData ={
                'userID': userID,
                'deviceID': deviceID,
                'username': username,
                'cardList': card_list
            }
        return JsonResponse(responseData, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_match_result(request):
    if request.method == 'POST':
        data = request.POST
        userID = [data['user1ID'], data['user2ID']]
        winner = data['winner']
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
        user1.trophy += calculate_trophy(user1.trophy, user1.level, True)

        user2.loseCount += 1
        user2.trophy += calculate_trophy(user2.trophy, user2.level, False)

        user1.save()
        user2.save()
        highscore_lb = Leaderboard('TheTree')
        highscore_lb.delete_leaderboard()
        highscore_lb.rank_member(user1.username, user1.trophy, user1.idUser)
        highscore_lb.rank_member(user2.username, user2.trophy, user2.idUser)
        print(highscore_lb.top(10))

        responseData = {
                'user1': {
                    'userID': user1.idUser,
                    'trophy': user1.trophy
                },
                'user2': {
                    'userID': user2.idUser,
                    'trophy': user2.trophy
                },
                'winner': winner
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
        print(top_100)
        responseData = {
                "top": top_100
            }
        return JsonResponse(responseData, status=status.HTTP_200_OK,encoder=MyEncoder)


def calculate_trophy(user_trophy, user_level, is_winner):
    return 10 if is_winner else -10


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, bytes):
          return obj.decode()
       return json.JSONEncoder.default(self, obj)
