from typing import Union

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class RangeValidator:

    def __init__(self, min_range=0, max_range=10, message=None):
        self.min_range = min_range
        self.max_range = max_range
        self.message = message
        if not message:
            self.message = "Value must bi in range %s - %s" % (self.min_range,self.max_range)

    def __call__(self, value):
        if not (self.min_range <= value <= self.max_range):
            raise ValidationError(message=self.message)

    @property
    def min_range(self):
        return self.__min_range

    @min_range.setter
    def min_range(self, value: Union[int,float]):
        if isinstance(value, (int,float)):
            self.__min_range = value
            return
        raise ValueError("Min range must be int or float.")

    @property
    def max_range(self):
        return self.__max_range


    @max_range.setter
    def max_range(self, value):
        if isinstance(value, (int, float)):
            self.__max_range = value
            return
        raise ValueError("Max range must be int or float.")