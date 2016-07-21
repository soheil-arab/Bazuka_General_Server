__author__ = 'soheil'

class CardUpgrade:
    @staticmethod
    def required_cards(card_level):
        if card_level is 10:
            return -1
        number_of_cards_required = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]
        return number_of_cards_required[card_level]

    @staticmethod
    def required_golds(card_level, rarity):
        if card_level is 10:
            return -1
        if rarity is 0:
            golds = [0, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        elif rarity is 1:
            golds = [0, 30, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
        elif rarity is 2:
            golds = [0, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000]
        else:
            return None
        return golds[card_level+1]

    @staticmethod
    def earned_xp(card_level, rarity):
        if card_level is 10:
            return -1
        if rarity is 0:
            xp = [0, 4, 6, 8, 10, 20, 50, 100, 200, 400, 600]
        elif rarity is 1:
            xp = [0, 10, 20, 50, 100, 200, 400, 600, 800, 1000, 2000]
        elif rarity is 2:
            xp = [0, 20, 100, 200, 500, 1000, 2000, 5000, 7000, 10000, 15000]
        else:
            return None
        return xp[card_level+1]

class CardPack:

    @staticmethod
    def pack_info(pack_type, league_level):
        if pack_type is 0:#kilo
            number_of_cards = [3, 4, 5, 6, 7, 8, 9, 12]
            min_golds = [15, 22, 25, 30, 35, 40, 35, 55]
            max_golds = [20, 27, 30, 35, 40, 45, 50, 70]
            rare_exp  = [0, 0, 0, 0, 0, 0, 0, 0]
            epic_exp  = [0, 0, 0, 0, 0, 0, 0, 0]
            type_count = [2, 2, 2, 2, 2, 2, 2, 2]
        elif pack_type is 1:#mega
            number_of_cards = [10, 14, 17, 20, 23, 26, 29, 40]
            min_golds = [50, 65, 75, 90, 105, 120, 135, 165]
            max_golds = [60, 75, 85, 100, 115, 130, 145, 200]
            rare_exp  = [1, 1, 1, 2, 2, 2, 2, 3]
            epic_exp  = [0, 0, 0, 0, 0, 0, 0, 0]
            type_count = [2, 2, 3, 3, 3, 3, 3, 3]

        elif pack_type is 2:#giga
            number_of_cards = [20, 27, 34, 40, 47, 55, 62, 75]
            min_golds = [100, 130, 165, 210, 250, 290, 310, 360]
            max_golds = [130, 160, 200, 250, 285, 320, 350, 430]
            rare_exp  = [2, 2, 3, 4, 4, 5, 6, 8]
            epic_exp  = [0, 0, 0, 0, 0, 0, 0, 0]
            type_count = [3, 3, 3, 3, 3, 3, 3, 3]

        elif pack_type is 3:#super_mega
            number_of_cards = [30, 40, 50, 60, 70, 80, 90, 120]
            min_golds = [155, 205, 255, 305, 355, 405, 455, 550]
            max_golds = [200, 250, 300, 350, 400, 450, 500, 650]
            rare_exp  = [5, 7, 8, 10, 12, 14, 15, 20]
            epic_exp  = [1, 1, 2, 2, 2, 3, 3, 5]
            type_count = [3, 4, 4, 4, 4, 5, 5, 5]

        elif pack_type is 4:#super_giga
            number_of_cards = [60, 90, 120, 150, 180, 210, 240, 300]
            min_golds = [300, 400, 500, 600, 700, 800, 900, 1100]
            max_golds = [400, 500, 600, 700, 800, 900, 1000, 1300]
            rare_exp  = [10, 12, 15, 18, 22, 25, 30, 40]
            epic_exp  = [3, 5, 7, 9, 11, 14, 16, 20]
            type_count = [3, 4, 4, 4, 5, 5, 5, 6]

        elif pack_type is 5:#tera
            number_of_cards = [200, 270, 340, 400, 470, 550, 620, 750]
            min_golds = [1200, 1500, 1800, 2100, 2500, 2800, 3100, 3600]
            max_golds = [1500, 1800, 2100, 2400, 2800, 3100, 3500, 4100]
            rare_exp  = [50, 70, 90, 110, 130, 160, 190, 250]
            epic_exp  = [0, 0, 0, 0, 0, 0, 0, 0]
            type_count = [5, 5, 6, 6, 6, 6, 6, 7]
        else:
            return None
        return number_of_cards[league_level], min_golds[league_level], max_golds[league_level],rare_exp[league_level],\
               epic_exp[league_level], type_count[league_level]

    @staticmethod
    def pack_time(pack_type, scale='H'):
        r = None
        if pack_type is 1:
            r = 3
        elif pack_type is 2:
            r = 7
        elif pack_type is 3:
            r = 10
        elif pack_type is 4:
            r = 12
        elif pack_type is 5:
            r = 16
        elif pack_type is 2:
            r = 24
        if scale is 'H':
            return r
        elif scale is 'M':
            return r*60
        elif scale is 'S':
            return r*60*60
