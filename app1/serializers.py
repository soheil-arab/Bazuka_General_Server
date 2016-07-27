__author__ = 'soheil'
from app1.models import User, Clan, CardType, Card, RewardPack, Donation

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

class ClanMinimalSerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField()

    def get_user_count(self, clan):
        return clan.users.count()

    class Meta:
        model = Clan
        fields = ('idClan', 'clanName', 'clanLocation', 'clanType', 'clanMinimumTrophies', 'clanScore', 'clanBadge',
                  'user_count')

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
    pack_content_info = serializers.SerializerMethodField()
    # def unlock_gem(self, pack):
    #     return 1

    def get_pack_remaining_time(self, pack):
        if pack.unlockStartTime is -1:
            return -1

        return CardPack.pack_time(pack.packType, 'S') - int(time.time()) + pack.unlockStartTime

    def get_pack_unlock_time(self, pack):
        return CardPack.pack_time(pack.packType, 'H')

    def get_pack_content_info(self, pack):
        number_of_cards, min_golds, max_golds, rare_exp, epic_exp, type_count = CardPack.pack_info(pack.packType, pack.packLeagueLevel)
        return {
            'number_of_cards': number_of_cards,
            'min_gold': min_golds,
            'max_gold': max_golds,
            'rere_exp': rare_exp,
            'epic_exp': epic_exp,
        }

    class Meta:
        model = RewardPack
        fields = ('idPack', 'packType', 'pack_remaining_time', 'pack_unlock_time', 'packLeagueLevel', 'slotNumber', 'pack_content_info')


class UserSerializer(serializers.ModelSerializer):
    clan_name = serializers.CharField(source='userClan.clanName', read_only=True)
    clan_id = serializers.IntegerField(source='userClan.idClan', read_only=True)

    class Meta:
        model = User
        fields = ('idUser', 'username', 'winCount', 'loseCount', 'deck1', 'xp', 'level', 'clan_id',
                  'clan_name', 'totalDonations', 'trophiesCount', 'leagueLevel')


class SelfSerializer(serializers.ModelSerializer):
    clan_name = serializers.CharField(source='userClan.clanName', read_only=True)
    clan_id = serializers.IntegerField(source='userClan.idClan', read_only=True)
    cards = CardSerializer(many=True)
    rewardPacks = PackSerializer(many=True)
    # xp_data = serializers.SerializerMethodField()
    # trophy_data = serializers.SerializerMethodField()
    next_level_xp = serializers.SerializerMethodField()
    next_league_trophy = serializers.SerializerMethodField()
    
    def get_next_level_xp(self, user):
        return user.level_xp_relation(user.level + 1)
    
    def get_next_league_trophy(self, user):
        return user.league_trophy_relation(user.leagueLevel+1)

    def get_xp_data(self, user):
        return {
            'user_level': user.level,
            'next_level_xp': user.level_xp_relation(user.level + 1),
            'user_xp': user.xp,
            'user_earned_xp': 0,
            'user_level_up': 0
        }

    def get_trophy_data(self, user):
        return {
            'user_earned_trophy': 0,
            'user_trophy': user.trophiesCount,
            'user_league_level': user.leagueLevel,
            'user_league_level_up': 0
        }

    class Meta:
        model = User
        fields = ('idUser', 'username', 'winCount', 'loseCount', 'deck1', 'xp', 'next_level_xp', 'level', 'clan_id',
                   'clan_name', 'totalDonations', 'trophiesCount', 'leagueLevel', 'next_league_trophy', 'cards', 'gold',
                   'gem', 'rewardPacks')


class DonationSerializer(serializers.ModelSerializer):

    owner_userID = serializers.IntegerField(source='owner.idUser', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    card_type_id = serializers.IntegerField(source='cardType.Cardid')
    remaining_time = serializers.SerializerMethodField()

    def get_remaining_time(self, donation):
        remain = int(time.time()) - donation.startTime
    class Meta:
        model = Donation
        fields = ('owner_userID', 'owner_username', 'requiredCardCount', 'donatedCardCount', 'donators', 'card_type_id')

# class ClanCreatorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Clan
#         fields = ('clanName', 'clanDescription', 'clanLocation', 'clanLeader')

