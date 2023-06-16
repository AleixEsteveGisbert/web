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

    # game = forms.ModelChoiceField(queryset=Game.objects.values_list('name', flat=True))

    # name.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Server
        fields = ['name']


class MinecraftServerPropertiesForm(forms.Form):
    server_properties = forms.CharField(label='server.properties', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '25'}))


