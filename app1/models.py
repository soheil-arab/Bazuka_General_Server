from django.db import models
from django.contrib.postgres.fields import ArrayField,HStoreField
from django.http import Http404
import random
from django.contrib.auth.models import User as djangoUser

CARD_RARITY = ((0, 'Common'), (1, 'Rare'), (2, 'Epic'))

def default_deck_gen():
    return random.choice([
        [15, 3, 5, 7, 9, 2, 16, 12],
        [6, 17, 8, 1, 11, 14, 16, 18],
        [12, 17, 15, 5, 19, 13, 6, 14]
    ])

def default_pack_cycle():
    return [120, 30, 10, 5, 2, 1]


def clan_tag_generator():
    return 'hi'

def probability_by_rarity(rarity):
    rarity_map={
        0: 200,
        1: 20,
        2: 1
    }
    return rarity_map[rarity]

class User(models.Model):
    idUser = models.AutoField(primary_key=True)
    deviceID = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=40, blank=True, default='')
    userCards = models.ManyToManyField('app1.CardType', through='Card')
    trophiesCount = models.IntegerField(default=0)
    winCount = models.IntegerField(default=0)
    loseCount = models.IntegerField(default=0)
    deck1 = ArrayField(models.IntegerField(), size=8, null=True, blank=True, default=default_deck_gen)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    leagueLevel = models.IntegerField(default=0)
    userClan = models.ForeignKey('app1.Clan', on_delete=models.SET_NULL, related_name='users', null=True, blank=True)
#    userTag = models.CharField(max_length=10, unique=True, db_index=True)
#    highestTrophies = models.IntegerField(default=0)
#    favoriteCard = models.IntegerField()
    totalDonations = models.IntegerField(default=0)
    gem = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)
    clanData = models.OneToOneField('app1.UserClanData', blank=True, null=True)
    basicUser = models.OneToOneField(djangoUser, related_name='user', blank=True, null=True, unique=True)
    packCycle = ArrayField(models.IntegerField(), size=6, default=default_pack_cycle)
    kingHP = models.SmallIntegerField(default=200)
    packCount = models.SmallIntegerField(default=0)
    packEmptySlots = ArrayField(models.IntegerField(), size=4, default=[1, 1, 1, 1])
    backtory_instanceID = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return 'user_{0}@{1}'.format(self.idUser, self.username)

    @staticmethod
    def get_object(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_random_pack(self):
        """

        :return:
        @:rtype RewardPack
        """
        if self.packCount >= 4:
            return None
        pack_cycle = self.packCycle
        pack_sum = sum(pack_cycle)
        if pack_sum is 0:
            pack_cycle = default_pack_cycle()
            pack_sum = sum(pack_cycle)
        index = random.randrange(0, pack_sum) + 1
        cum_sum = 0
        for idx, item in enumerate(pack_cycle):
            cum_sum += item
            if index <= cum_sum:
                pack_cycle[idx] -= 1
                self.packCycle = pack_cycle
                # self.save()
                tmp_pack = RewardPack()
                tmp_pack.packLeagueLevel = self.leagueLevel
                tmp_pack.packType = idx
                tmp_pack.packUser = self.idUser
                tmp_pack.save()
                return tmp_pack
        #
        # TODO:prevent Error

    def add_xp(self, earned_xp):
        next_xp = self.level_xp_relation(self.level+1)
        self.xp += earned_xp
        level_up = False
        if self.xp >= next_xp > -1:
            level_up = True
            self.level += 1
            self.xp -= next_xp
            self.kingHP = self.level_kinghp_relation(self.level)
        # self.save()
        data = {
            'user_level': self.level,
            'next_level_xp': self.level_xp_relation(self.level + 1),
            'user_xp': self.xp,
            'user_earned_xp': earned_xp,
            'user_level_up': 1 if level_up else 0
        }
        return data

    def add_trophy(self, earned_trophy):
        self.trophiesCount += earned_trophy
        level_up = 0
        next_league_trophy = self.league_trophy_relation(self.leagueLevel+1)
        curr_league_trophy = self.league_trophy_relation(self.leagueLevel)
        if self.trophiesCount < curr_league_trophy - 50:
            self.leagueLevel -= 1
            level_up = -1
        elif self.trophiesCount >= next_league_trophy:
            self.leagueLevel += 1
            level_up = +1

        # self.save()
        data = {
            'user_earned_trophy': earned_trophy,
            'user_trophy': self.trophiesCount,
            'user_league_level': self.leagueLevel,
            'user_league_level_up': level_up
        }
        return data

    def add_cards(self, earned_cards):
        cards = []
        for card_type in earned_cards:
            try:
                cardT = CardType.objects.get(Cardid=card_type)
            except CardType.DoesNotExist:
                print('fuck you')
                return None

            try:
                x = self.cards.all().get(cardType=cardT)
                x.cardCount += earned_cards[card_type]
                print('old card')
            except Card.DoesNotExist:
                x = Card()
                x.cardCount = earned_cards[card_type]
                x.cardLevel = 0
                x.cardType = cardT
                x.user = self
                print('new card')

            x.save()
            cards.append(x)
        return cards

    def add_gold(self, earned_gold):
        self.gold += earned_gold
        data = {
            'earned_gold': earned_gold,
            'user_gold': self.gold
        }
        return data

    def add_gem(self, earned_gem):
        self.gem += earned_gem
        data = {
            'earned_gem': earned_gem,
            'user_gem': self.gem
        }
        return data

    @staticmethod
    def level_xp_relation(level):
        if level >= 11:
            return -1
        x = {
            0: 0, 1: 10,
            2: 20, 3: 50,
            4: 100, 5: 200,
            6: 500, 7: 1000,
            8: 2000, 9: 5000,
            10: 10000
        }
        return x[level]

    @staticmethod
    def level_kinghp_relation(level):
        if -1 >= level or level >= 11:
            return -1
        x = {
            0: 200, 1: 220,
            2: 242, 3: 266,
            4: 293, 5: 322,
            6: 354, 7: 389,
            8: 428, 9: 471,
            10: 518
        }
        return x[level]

    @staticmethod
    def league_trophy_relation(league):
        x = {
            0: 0,
            1: 100, 2: 400,
            3: 700, 4: 1000,
            5: 1400, 6: 1700,
            7: 2000, 8: 3000
        }
        return x[league]


class CardType(models.Model):
    idCardType = models.AutoField(primary_key=True)
    Cardid = models.IntegerField(unique=True, db_index=True, null=True)
    cardName = models.CharField(max_length=40)
    cardRarity = models.SmallIntegerField(choices=CARD_RARITY, default=0)
    cardLeagueLevel = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.cardName

    @staticmethod
    def get_available_cards(leagueLevel):
        card_list = CardType.objects.filter(cardLeagueLevel__lte=leagueLevel)
        avail_cards = list()
        cards_prob = dict()
        for card in card_list:
            avail_cards.append(card.Cardid)
            cards_prob[card.Cardid] = probability_by_rarity(card.cardRarity)
        return avail_cards, cards_prob

    @staticmethod
    def get_available_epic_rare_cards(leagueLevel):
        rare = CardType.objects.filter(cardLeagueLevel__lte=leagueLevel).filter(cardRarity__gte=1)
        rare_list = list()
        for card in rare:
            rare_list.append(card.Cardid)
        epic = rare.filter(cardRarity__gte=2)
        epic_list = list()
        for card in epic:
            epic_list.append(card.Cardid)
        return epic_list, rare_list

    @staticmethod
    def get_league_cards(leagueLevel):
        return CardType.objects.filter(cardLeagueLevel=leagueLevel)

    # @staticmethod
    # def get_available_cards_with_prob(leagueLevel):
    #     cards = CardType.get_available_cards(leagueLevel)
    #     total = 0
    #     for card in cards:
    #         total += probability_by_rarity(card.cardRarity)
    #     prob_list = list()
    #     for card in cards:
    #         prob_list.append(probability_by_rarity(card.cardRarity)/total)
    #     return cards, prob_list

class Clan(models.Model):
    idClan = models.AutoField(primary_key=True)
    clanName = models.CharField(max_length=30)
    clanDescription = models.TextField(max_length=140, blank=True, null=True)
    clanTag = models.CharField(max_length=10, unique=True, db_index=True, blank=True, null=True)#TODO: generate clan tag
    clanLocation = models.CharField(max_length=50, blank=True, null=True)
    clanType = models.IntegerField(default=0)
    clanMinimumTrophies = models.IntegerField(default=0)
    clanScore = models.IntegerField(default=0)
    totalDonation = models.IntegerField(default=0) #TODO: change to donation per week
    clanBadge = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return 'clan_{0}@{1}'.format(self.idClan, self.clanName)

class RewardPack(models.Model):
    idPack = models.AutoField(primary_key=True)
    packType = models.IntegerField(default=0)
    unlockStartTime = models.IntegerField(default=-1)
    packLeagueLevel = models.IntegerField(default=0)
    packUser = models.ForeignKey('app1.User', on_delete=models.CASCADE, related_name='rewardPacks')
    slotNumber = models.IntegerField(blank=True, null=True)

    @staticmethod
    def get_object(pk):
        try:
            return RewardPack.objects.get(pk=pk)
        except RewardPack.DoesNotExist:
            raise Http404


class Card(models.Model):
    idCard = models.AutoField(primary_key=True)
    cardLevel = models.SmallIntegerField(default=1)
    cardCount = models.SmallIntegerField(default=0)
    cardType = models.ForeignKey(CardType, on_delete=models.CASCADE, related_name='cards')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')

    class Meta:
        unique_together = (('user', 'cardType'), )
        index_together = [['user', 'cardType'], ]



class UserClanData(models.Model):
    POSITION_CHOICES = (
        (0, 'Member'),
        (1, 'Leader'),
    )
    position = models.IntegerField(default=0, choices=POSITION_CHOICES)
    donate_count = models.IntegerField(default=0)
    lastRequestTime = models.IntegerField(default=0)



class Donation(models.Model):
    owner = models.ForeignKey(User)
    requiredCardCount = models.IntegerField(default=0)
    donatedCardCount = models.IntegerField(default=0)
    donators = HStoreField()
