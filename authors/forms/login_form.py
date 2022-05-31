from django import forms


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Type your username"
        self.fields["password"].widget.attrs["placeholder"] = "Type your password"

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
