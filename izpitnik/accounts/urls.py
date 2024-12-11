from django.urls import path, include

from izpitnik.accounts.views import MainLoginView, MainLogoutView, MainSignUpView, ProfilePage, ProfileEditPage, \
    MainProfileDeleteView

urlpatterns = [
    path('login/', MainLoginView.as_view(), name='login-page'),
    path('logout/', MainLogoutView.as_view(), name='logout-page'),
    path('register/', MainSignUpView.as_view(), name='register-page'),
    path('profile/', ProfilePage.as_view(), name='profile-page'),
    path('profile/edit/', ProfileEditPage.as_view(), name='profile-edit-page'),
    path('profile/delete/', MainProfileDeleteView.as_view(), name='profile-delete-page'),
]
