from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView, DetailView
from unfold.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from izpitnik.accounts.decorators import set_message
from izpitnik.accounts.forms import MainUserCreationForm, ProfileForm
from izpitnik.accounts.models import Profile


# Create your views here.

class MainLoginView(UserPassesTestMixin, LoginView):

    def test_func(self):
        return not self.request.user.is_authenticated

    @set_message(_('You have successfully logged in!'))
    def get_success_url(self):
        return super().get_success_url()

    template_name = 'accounts/login.html'
    next_page = 'home-page'
    redirect_authenticated_user = True

class MainLogoutView(UserPassesTestMixin,LogoutView):

    def test_func(self):
        return self.request.user.is_authenticated

    @set_message(_('You have successfully logged out!'))
    def get_success_url(self):
        return super().get_success_url()

    template_name = 'accounts/logout.html'
    next_page = 'login-page'

class MainSignUpView(UserPassesTestMixin,CreateView):

    def test_func(self):
        return not self.request.user.is_authenticated

    form_class = MainUserCreationForm
    success_url = reverse_lazy('login-page')
    template_name = 'accounts/register.html'

class ProfilePage(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_object(self, queryset = None):
        return Profile.objects.filter(user__pk=self.request.user.pk).first()


class ProfileEditPage(UserPassesTestMixin,LoginRequiredMixin,UpdateView):

    # def test_func(self):
    #     if self.request.user.is_superuser:
    #         return True
    #     return self.request.user.pk == self.get_uid()
    #
    # def get_uid(self):
    #     try:
    #         return int(self.request.GET.get('uid', -1))
    #     except ValueError:
    #         return -1

    def test_func(self):
        return bool(self.get_object())

    form_class  = ProfileForm
    template_name = 'accounts/profile-edit.html'
    success_url = reverse_lazy('profile-edit-page')

    def get_object(self, queryset = None):
        # user = self.get_uid()
        return Profile.objects.filter(user__pk=self.request.user.pk).first()




