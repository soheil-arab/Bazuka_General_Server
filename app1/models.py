from django.db import models
from django.contrib.postgres.fields import ArrayField
import random

def default_deck_gen():
    return random.choice([
        [5, 3, 8, 11, 12, 13, 16, 18],
        [2, 3, 6, 7, 12, 14, 17, 18],
        [5, 1, 2, 3, 9, 15, 16, 19]
    ])

class CardType(models.Model):
    idCardType = models.AutoField(primary_key=True)
    Cardid = models.IntegerField(unique=True, db_index=True, null=True)
    name = models.CharField(max_length=40)
    # CARD_RARITY = ((0, 'Common'), (1, 'Rare'), (2, 'Epic'))
    # rarity = models.SmallIntegerField(choices=CARD_RARITY)

    def __str__(self):
        return self.name

class User(models.Model):
    idUser = models.AutoField(primary_key=True)
    idDevice = models.CharField(max_length=200)
    username = models.CharField(max_length=40, blank=True, default='')
    cardID = models.ManyToManyField(CardType, through='Card')
    trophy = models.IntegerField(default=0)
    winCount = models.IntegerField(default=0)
    loseCount = models.IntegerField(default=0)
    deck1 = ArrayField(models.IntegerField(), size=8, null=True, blank=True, default=default_deck_gen)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    def __str__(self):
        return 'user_{0}@{1}'.format(self.idUser,self.username)


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


