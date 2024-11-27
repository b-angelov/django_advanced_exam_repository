from datetime import datetime, date as dt
from pyexpat.errors import messages
from typing import Union

from izpitnik.orth_calendar.utils.easterlib import EasterCalculus


class ChristmasCalculus:

    ALLOWED_CALENDARS = ["Julian","Gregorian"]
    CHRISTMAS_DATES = {
        "Julian": (1,7),
        "Gregorian": (12,25),
    }

    def __init__(self, date: dt, calendar: str = "Gregorian"):
        """
        allowed
        :param date: datetime object of the day, to be checked
        :param calendar: String value for leap year check should be "Gregorian" or "Julian"
        """
        self.date = date
        self.is_leap = EasterCalculus.isLeap(date.year, calendar)
        self.leap_day = self.get_leap_day()
        self.calendar = calendar
        self.christmas_date = self.get_christmas_date(calendar)

    def get_christmas_date(self, calendar):
        return dt(self.date.year - 1,*self.CHRISTMAS_DATES.get(calendar,self.CHRISTMAS_DATES["Gregorian"]))

    def get_leap_day(self):
        if self.is_leap:
            try:
                return dt(self.date.year,2,29)
            except ValueError:
                return

    def christmas_distance(self):
        if self._skip():
            return
        leap_day = self.get_leap_day()
        days = self.date - self.christmas_date
        days = ((365 + days.days) % 365) + 1
        if leap_day and self.date > leap_day:
            days -=1
        return days

    def _skip(self):
        leap_day = self.get_leap_day()
        if leap_day == self.date:
            return True


    def __repr__(self):
        return str(self.christmas_distance())

    @property
    def calendar(self):
        return self.__calendar

    @calendar.setter
    def calendar(self, value):
        if value not in self.ALLOWED_CALENDARS:
            raise ValueError(f"Calendar value should be in allowed calendar list - {', '.join(self.ALLOWED_CALENDARS)}")
        self.__calendar = value
