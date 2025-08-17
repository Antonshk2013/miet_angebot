from src.commons.choices.base import BaseChoice


class CountRumsChoice(BaseChoice):
    one_rums = 'one_rums'
    two_rums = 'two_rums'
    three_rums = 'three_rums'
    gte_four_rums = 'four und mer'


    @classmethod
    def get_imap(cls):
        return {
            1: "one_rums",
            2: "two_rums",
            3: "three_rums",
            4: "gte_four_rums",
        }

    @classmethod
    def filter_by_int_map(cls, min_value=None, max_value=None):
        if min_value:
            min_value = int(min_value)
        if max_value:
            max_value = int(max_value)
        data = cls.get_imap()
        result = [
            v for k, v in data.items()
            if (min_value is None or k >= min_value)
               and (max_value is None or k <= max_value)
        ]
        return result

