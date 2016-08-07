__author__ = 'soheil'

class DonationConf():

    @staticmethod
    def donate_request_period():
        return 8 * 60 * 60

    @staticmethod
    def donate_reward(card_type_id):
        """

        :param card_type_id:
        :return: earned_xp, earned_gold
        """
        if card_type_id == 0:
            return 1, 5
        elif card_type_id == 1:
            return 10, 50

    @staticmethod
    def max_donate_count(league_level, card_type_id):
        """

        :param league_level:
        :param card_type_id:
        :return:
        """
        common = [1, 2, 2, 4, 4, 6, 6, 8]
        rare = [1, 1, 1, 1, 1, 1, 1, 1]
        if card_type_id is 0:
            return common[league_level]
        elif card_type_id is 1:
            return rare[league_level]

    @staticmethod
    def donate_request_capacity(league_level, card_type_id):
        """

        :param league_level:
        :param card_type_id:
        :return:
        """
        common = [10, 10, 10, 20, 20, 20, 30, 30]
        rare = [1, 1, 1, 2, 2, 2, 3, 3]
        if card_type_id is 0:
            return common[league_level]
        elif card_type_id is 1:
            return rare[league_level]

    @staticmethod
    def daily_limit(league_level):
        count = [10, 10, 10, 20, 20, 20, 30, 30]
        return count[league_level] * 5