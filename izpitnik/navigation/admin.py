import unfold
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from prompt_toolkit.widgets import MenuItem

from izpitnik.navigation.forms import NavigationLanguageForm
from izpitnik.navigation.models import Navigation, Menu, Language


# Register your models here.


@admin.register(Navigation)
class NavigationAdmin(unfold.admin.ModelAdmin):

    list_display = ['item_name','url_external','url_internal']
    fields = [
        'menu','item_name',('url_internal','url_external'),'parent_id',"language","order"
    ]
    list_filter = [
        'menu',"menu__slug"
    ]
    class Meta:
        pass

@admin.register(Menu)
class NavigationMenuAdmin(unfold.admin.ModelAdmin):
    display_fields = (
        "cust_name"
    )

    @admin.display(description=_("menu"))
    def cust_name(self, obj):
        return _(obj.name)

@admin.register(Language)
class NavigationLanguageAdmin(unfold.admin.ModelAdmin):
    form = NavigationLanguageForm
    list_display =[
        "cust_name",
        "language_code",
    ]

    @admin.display(description=_("name"))
    def cust_name(self, obj):
        return _(obj.name)

    def has_add_permission(self, request):
        return False
