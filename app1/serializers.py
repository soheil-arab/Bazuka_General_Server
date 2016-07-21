__author__ = 'soheil'
from app1.models import User, Clan, CardType, Card, RewardPack

from rest_framework import serializers
from app1.card_conf import CardUpgrade, CardPack


import time

class CardSerializer(serializers.ModelSerializer):
    next_level_count = serializers.SerializerMethodField('next_count')
    next_level_gold = serializers.SerializerMethodField('next_gold')
    cardRarity = serializers.IntegerField(source='cardType.cardRarity')
    cardTypeID = serializers.IntegerField(source='cardType.Cardid')
    cardDBIndex = serializers.IntegerField(source='idCard')
    upgradable = serializers.SerializerMethodField('is_upgradable')
    isNewCard = serializers.SerializerMethodField('is_new_card')

    def is_new_card(self, card):
        return 0

    def is_upgradable(self, card):
        return 1 if card.cardCount >= self.next_count(card) else 0

    def next_count(self, card):
        return CardUpgrade.required_cards(card.cardLevel)

    def next_gold(self, card):
        return CardUpgrade.required_golds(card.cardLevel, card.cardType.cardRarity)

    class Meta:
        model = Card
        fields = ('cardTypeID', 'cardDBIndex', 'cardRarity', 'cardCount', 'cardLevel', 'next_level_count',
                  'next_level_gold', 'upgradable', 'isNewCard')

class ClanUserSerializer(serializers.ModelSerializer):
    donate_count = serializers.IntegerField(source='clanData.donate_count', read_only=True)
    position = serializers.IntegerField(source='clanData.position', read_only=True)

    class Meta:
        model = User
        fields = ('idUser', 'username', 'level', 'trophiesCount', 'position', 'donate_count')

class ClanSerializer(serializers.ModelSerializer):
    users = ClanUserSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Clan
        fields = ('idClan', 'clanName', 'clanDescription', 'clanLocation', 'clanType',
                  'clanMinimumTrophies', 'clanScore', 'users', 'clanBadge')


class PackSerializer(serializers.ModelSerializer):
    # unlock_required_gem = serializers.SerializerMethodField('unlock_gem')
    pack_remaining_time = serializers.SerializerMethodField()
    pack_unlock_time = serializers.SerializerMethodField()
    # def unlock_gem(self, pack):
    #     return 1

    def get_pack_remaining_time(self, pack):
        if pack.unlockStartTime is -1:
            return -1
        return CardPack.pack_time(pack.packType, 'S') - int(time.time()) + pack.unlockStartTime

    def get_pack_unlock_time(self, pack):
        return CardPack.pack_time(pack.packType, 'H')

    class Meta:
        model = RewardPack
        fields = ('idPack', 'packType', 'pack_remaining_time', 'pack_unlock_time', 'packLeagueLevel', 'slotNumber')


class UserSerializer(serializers.ModelSerializer):
    clan_name = serializers.CharField(source='userClan.clanName', read_only=True)
    clan_id = serializers.IntegerField(source='userClan.idClan', read_only=True)
    cards = CardSerializer(many=True)

    class Meta:
        model = User
        fields = ('idUser', 'username', 'winCount', 'loseCount', 'deck1', 'xp', 'level', 'clan_id',
                  'clan_name', 'totalDonations', 'trophiesCount', 'leagueLevel', 'cards', 'gold', 'gem')


class SelfSerializer(serializers.ModelSerializer):
    clan_name = serializers.CharField(source='userClan.clanName', read_only=True)
    clan_id = serializers.IntegerField(source='userClan.idClan', read_only=True)
    cards = CardSerializer(many=True)
    next_level_xp = serializers.SerializerMethodField('next_xp')
    next_league_trophy = serializers.SerializerMethodField('next_trophy')
    rewardPacks = PackSerializer(many=True)

    def next_xp(self, user):
        return user.level_xp_relation(user.level + 1)

    def next_trophy(self, user):
        return user.league_trophy_relation(user.leagueLevel+1)

    class Meta:
        model = User
        fields = ('idUser', 'username', 'winCount', 'loseCount', 'deck1', 'xp', 'next_level_xp', 'level', 'clan_id',
                  'clan_name', 'totalDonations', 'trophiesCount', 'leagueLevel', 'next_league_trophy', 'cards', 'gold',
                  'gem', 'rewardPacks')


# class ClanCreatorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Clan
#         fields = ('clanName', 'clanDescription', 'clanLocation', 'clanLeader')

