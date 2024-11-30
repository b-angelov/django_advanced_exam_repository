from datetime import datetime
from .utils.calculus import Calculus


def set_calculus(calendar='JIG'):
    def wrapper(func):
        def calculus(*args,**kwargs):
            cal = kwargs.get('calendar', calendar)
            date = datetime.strptime(kwargs.get('date',args[1]),'%Y-%m-%d').date()
            distance_dict = Calculus(date,calendar).get_distance()
            return func(*args,**kwargs,distance_dict=distance_dict)
        return calculus
    return wrapper