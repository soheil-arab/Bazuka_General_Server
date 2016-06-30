__author__ = 'soheil'
from app1.models import User, Clan, CardType, Card#, RewardPack

from rest_framework import serializers

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('cardType', 'cardCount', 'cardLevel')

class ClanUserSerializer(serializers.ModelSerializer):
    donate_count = serializers.IntegerField(source='clanData.donate_count', read_only=True)
    position = serializers.IntegerField(source='clanData.position', read_only=True)

    class Meta:
        model = User
        fields = ('idUser', 'username', 'level', 'trophiesCount', 'position', 'donate_count')

class ClanSerializer(serializers.ModelSerializer):
    users = ClanUserSerializer(many=True,required=False)

    class Meta:
        model = Clan
        fields = ('idClan', 'clanName', 'clanDescription', 'clanLocation', 'clanType',
                  'clanMinimumTrophies', 'clanScore', 'users')



class UserSerializer(serializers.ModelSerializer):
    clan_name = serializers.CharField(source='userClan.clanName', read_only=True)
    clan_id = serializers.IntegerField(source='userClan.idClan', read_only=True)
    cards = CardSerializer(many=True)

    class Meta:
        model = User
        fields = ('idUser', 'username', 'cards', 'trophiesCount', 'winCount', 'loseCount', 'deck1', 'xp', 'level',
                  'clan_id', 'clan_name', 'totalDonations')


class SelfSerializer(serializers.ModelSerializer):
    clan_name = serializers.CharField(source='userClan.clanName', read_only=True)
    clan_id = serializers.IntegerField(source='userClan.idClan', read_only=True)
    cards = CardSerializer(many=True)

    class Meta:
        model = User
        fields = ('idUser', 'username', 'cards', 'trophiesCount', 'winCount', 'loseCount', 'deck1', 'xp', 'level',
                  'clan_id', 'clan_name', 'totalDonations', 'basicUser')

# class PackSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = RewardPack
#         fields = ('packType', 'unlockStartTime', 'packLevel', 'packUser')

# class ClanCreatorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Clan
#         fields = ('clanName', 'clanDescription', 'clanLocation', 'clanLeader')

