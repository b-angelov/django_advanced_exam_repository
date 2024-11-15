from django.db import models
from django.urls import reverse
from prompt_toolkit.validation import ValidationError


# Create your models here.


class Navigation(models.Model):

    slug = models.SlugField(max_length=50,blank=False,null=False)
    item_name = models.CharField(max_length=50, blank=False,null=False)
    url_external = models.URLField(blank=True, null=True)
    url_internal = models.SlugField(blank=True, null=True)
    parent_id = models.ForeignKey(to='Navigation', null=True, blank=True, related_name="children", on_delete=models.SET(-1))

    class Meta:
        unique_together = ('slug', 'url_external', 'url_internal')

    def __str__(self):
        return self.item_name

    def resolved_url(self):
        try:
            url = self.url_internal
            if url:
                url = reverse(self.url_internal)
        except:
            url = self.url_external
        return url
