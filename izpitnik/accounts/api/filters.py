

def filter_user_response(func):
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        if (
                not request.user.is_authenticated
                or str(request.user.pk) != kwargs.get(self.lookup_url_kwarg)
                or not request.user.has_perm("accounts.view_user")
                or not request.user.is_superuser
        ):
            response.data = {k:v for k,v in response.data.items() if k in ['username','first_name','last_name','profile']}
        return response
    return wrapper