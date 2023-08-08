from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

from Web_App.models import UserInfo, Wallet, Server, Game


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'usuari", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuari'}))
    password = forms.CharField(label="Contrasenya", max_length=30, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'contrasenya'}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correu", required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'exemple@gmail.com'}))
    username = forms.CharField(label="Nom d'usuari",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuari'}))
    password1 = forms.CharField(label="Contrasenya", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'contrasenya'}))
    password2 = forms.CharField(label="Repeteix la contrasenya", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'contrasenya'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            wallet = Wallet.objects.create()
            userInfo = UserInfo.objects.create(user=user, wallet=wallet, avatar='avatars/default_avatar.png')

        return user


class NewServerForm(forms.ModelForm):
    name = forms.CharField(label="Nom del server",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom del server'}))
    # cores = forms.IntegerField(label="Nuclis CPU", widget=forms.NumberInput(attrs={'type':'range', 'class': 'form-range', 'min': '1', 'max': '8', 'step': '2', 'value': '1'}), min_value=1, max_value=8, step_size=1)
    # ram = forms.IntegerField(label="RAM", widget=forms.NumberInput(attrs={'type':'range', 'data-slider-ticks-labels': '["short", "medium", "long"]', 'class': 'form-range', 'min': '2', 'max': '10', 'step': '2', 'value': '2'}), min_value=2, max_value=10, step_size=2)

    cores = forms.ChoiceField(choices=[('1', '1'), ('2', '2'), ('4', '4')], widget=forms.Select(attrs={'class': 'form-select'}))
    ram = forms.ChoiceField(choices=[('1', '1'), ('2', '2'), ('4', '4'), ('6', '6'), ('8', '8')], widget=forms.Select(attrs={'class': 'form-select'}))
    game = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), queryset=Game.objects.all())

    # name.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Server
        fields = ['name', 'cores', 'ram', 'game']


class MinecraftServerPropertiesForm(forms.Form):
    server_properties = forms.CharField(label='server.properties', widget=forms.Textarea(attrs={'class': 'form-control bg-dark text-light', 'rows': '25'}))

class addDaysForm(forms.Form):
    days = forms.ChoiceField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')],
                            widget=forms.Select(attrs={'class': 'form-select'}))
