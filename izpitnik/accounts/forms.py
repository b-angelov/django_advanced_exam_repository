import unfold.forms as forms
from django.contrib.auth import get_user_model


class MainUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)



class MainUserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = get_user_model()
        fields = '__all__'
