from django.contrib import admin

from izpitnik.navigation.models import Navigation


# Register your models here.


@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):

    list_display = ['item_name','slug','url_external','url_internal']
    fields = [
        'slug','item_name',('url_internal','url_external'),'parent_id'
    ]
    class Meta:
        pass
