from datetime import date

from izpitnik.orth_calendar.utils.christmaslib import ChristmasCalculus
from izpitnik.orth_calendar.utils.easterlib import EasterCalculus


class Calculus(ChristmasCalculus):

    TRANSLATIONS = {
        "J":"Julian",
        "G":"Gregorian",
        "JIG":"JulianInGregorian"
    }

    def __init__(self,*args,**kwargs):
        self.ALLOWED_CALENDARS.append("JulianInGregorian")
        args = list(args)
        calendar = kwargs.get("calendar",args.pop(1))
        kwargs["calendar"] = self.TRANSLATIONS.get(calendar,calendar)
        super().__init__(*args,**kwargs)
        easter_date = EasterCalculus(self.date.year,self.calendar).date
        self.easter_date = date(easter_date[2],easter_date[0],easter_date[1])

    def easter_distance(self):
        if self._skip():
            return
        days = (self.date - self.easter_date).days
        if self.is_leap and self.date < self.get_leap_day():
            days += 1
        return days

    def get_distance(self):
        return {"christmas":self.christmas_distance(), "easter":self.easter_distance()}
