from rest_framework.generics import ListAPIView

from izpitnik.navigation.models import Navigation, Menu
from izpitnik.navigation.serializers import NavigationSerializer, MenuSerializer


class NavigationApiView(ListAPIView):
    serializer_class = NavigationSerializer
    lookup_url_kwarg = "nav_name"

    def get_queryset(self):
        menu = Menu.objects.prefetch_related("navigation","navigation__menu","navigation__language","navigation__children").filter(slug=self.kwargs['nav_name']).order_by("pk").first()
        if not menu:
            return Navigation.objects.none()
        items = menu.navigation.filter(language__language_code__icontains=self.request.GET.get("lang") or "bg").order_by("order","pk")
        user = self.request.user
        uid = ''
        if not user.is_authenticated:
            items = items.filter(login_required=False)
        else:
            items = items.filter(anonymous_required=False)
            uid = f'?uid={user.pk}'
        items = filter(lambda item: not item.permission_required or user.has_perm(item.permission_required.codename),
                       items)
        return items
