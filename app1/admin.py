from django.contrib import admin
from .models import *
# Register your models here.
class CardInline(admin.TabularInline):
    model = Card

class UserAdmin(admin.ModelAdmin):
    inlines = (CardInline,)

admin.site.register(Card)
admin.site.register(User, UserAdmin)
admin.site.register(Clan)
admin.site.register(UserClanData)