from django.contrib.auth.mixins import UserPassesTestMixin


class IsAuthor(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.has_perm("articles.change_article"):
            return True
        return self.get_object().author.pk == self.request.user.pk