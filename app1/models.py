from django.db import models
from django.contrib.postgres.fields import ArrayField
import random

def default_deck_gen():
    return random.choice([
        [0, 3, 8, 11, 12, 13, 16, 18],
        [2, 3, 6, 7, 12, 14, 17, 18],
        [0, 1, 2, 4, 9, 15, 16, 19]
    ])

def clan_tag_generator():
    return 'hi'

class CardType(models.Model):
    idCardType = models.AutoField(primary_key=True)
    Cardid = models.IntegerField(unique=True, db_index=True, null=True)
    name = models.CharField(max_length=40)
    # CARD_RARITY = ((0, 'Common'), (1, 'Rare'), (2, 'Epic'))
    # rarity = models.SmallIntegerField(choices=CARD_RARITY)

    def __str__(self):
        return self.name

class Clan(models.Model):
    idClan = models.AutoField(primary_key=True)
    clanName = models.CharField(max_length=30)
    clanDescription = models.TextField(max_length=140, blank=True, null=True)
    clanTag = models.CharField(max_length=10, unique=True, db_index=True, blank=True, null=True)#TODO: generate clan tag
    clanLocation = models.CharField(max_length=30, blank=True, null=True)
    clanType = models.IntegerField(default=0)
    clanMinimumTrophies = models.IntegerField(default=0)
    clanScore = models.IntegerField(default=0)
    totalDonation = models.IntegerField(default=0) #TODO: change to donation per week
    clanBadge = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return 'clan_{0}@{1}'.format(self.idClan, self.clanName)

class User(models.Model):
    idUser = models.AutoField(primary_key=True)
    deviceID = models.CharField(max_length=200)
    username = models.CharField(max_length=40, blank=True, default='')
    userCards = models.ManyToManyField(CardType, through='Card')
    trophiesCount = models.IntegerField(default=0)
    winCount = models.IntegerField(default=0)
    loseCount = models.IntegerField(default=0)
    deck1 = ArrayField(models.IntegerField(), size=8, null=True, blank=True, default=default_deck_gen)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    userClan = models.ForeignKey('app1.Clan', on_delete=models.SET_NULL, related_name='users', null=True, blank=True)
#    userTag = models.CharField(max_length=10, unique=True, db_index=True)
#    highestTrophies = models.IntegerField(default=0)
#    favoriteCard = models.IntegerField()
    totalDonations = models.IntegerField(default=0)
    gem = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)
    clanData = models.OneToOneField('app1.UserClanData', blank=True, null=True)

    def __str__(self):
        return 'user_{0}@{1}'.format(self.idUser, self.username)

class RewardPack(models.Model):
    packType = models.IntegerField(default=0)
    unlockStartTime = models.IntegerField()
    packLevel = models.IntegerField()
    packUser = models.ForeignKey('app1.User', on_delete=models.CASCADE, related_name='rewardPacks')

class Card(models.Model):
    idCard = models.AutoField(primary_key=True)
    cardLevel = models.SmallIntegerField(default=1)
    cardCount = models.SmallIntegerField(default=0)
    cardType = models.ForeignKey(CardType, on_delete=models.CASCADE, related_name='cards')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')

    class Meta:
        unique_together = (('user', 'cardType'), )
        index_together = [['user', 'cardType'], ]

# class Deck(models.Model):
#     idDeck = models.AutoField(primary_key=True)
#     cardID = models.ManyToManyField(Card)
#     user = models.ForeignKey(User, related_name='decks')
#     deckNum = models.PositiveSmallIntegerField()
#
#     class Meta:
#         unique_together = (('user', 'deckNum'), )
#         index_together = [['user', 'deckNum']]




class UserClanData(models.Model):
    POSITION_CHOICES = (
        (0, 'Member'),
        (1, 'Leader'),
    )
    position = models.IntegerField(default=0, choices=POSITION_CHOICES)
    donate_count = models.IntegerField(default=0)
    lastRequestTime = models.IntegerField(default=0)

