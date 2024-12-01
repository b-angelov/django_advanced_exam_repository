from datetime import datetime
from .utils.calculus import Calculus


def set_calculus(calendar='JIG'):
    def wrapper(func):
        def calculus(*args,**kwargs):
            cal = kwargs.get('calendar', calendar) or calendar
            date = datetime.strptime(kwargs.get('date',args[1]),'%Y-%m-%d').date()
            distance_obj = {'obj':Calculus, 'data':{'date':date,'calendar':cal}}
            kwargs['distance_obj'] = distance_obj
            return func(*args,**kwargs)
        return calculus
    return wrapper


