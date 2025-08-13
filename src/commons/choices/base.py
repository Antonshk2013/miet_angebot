from enum import Enum


class BaseChoice(str, Enum):

    @classmethod
    def choices(cls):
        return [(i.value, i.value) for i in cls]

