import unfold.forms as forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm

from izpitnik.accounts.models import Profile


class MainUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)



class MainUserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = get_user_model()
        fields = '__all__'


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude=('pk','user')
