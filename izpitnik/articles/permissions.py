from django.contrib.auth.mixins import UserPassesTestMixin


class IsAuthor(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return self.get_object().author.pk == self.request.user.pk