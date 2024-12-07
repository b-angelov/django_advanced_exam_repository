from django.contrib import messages
from django.contrib.messages.api import add_message



def set_message(message="",level=200,extra_tags=''):
    def inner(func):
        def wrapper(self,*args, **kwargs):
            add_message(self.request,level,message,extra_tags,fail_silently=False)
            return func(self, *args,**kwargs)
        return wrapper
    return inner