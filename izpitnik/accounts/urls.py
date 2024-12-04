from django.urls import path, include

from izpitnik.accounts.views import MainLoginView, MainLogoutView, MainSignUpView

urlpatterns = [
    path('login/', MainLoginView.as_view(), name='login-page'),
    path('logout/', MainLogoutView.as_view(), name='logout-page'),
    path('register/', MainSignUpView.as_view(), name='register-page'),
]
