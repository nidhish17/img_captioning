from django import forms
from .models import Account


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "your password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "confirm password", "class": "form-control"}))
    confirm_email = forms.EmailField()

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "your firstname"
        self.fields["last_name"].widget.attrs["placeholder"] = "your lastname"
        self.fields["email"].widget.attrs["placeholder"] = "example@example.com"
        self.fields["confirm_email"].widget.attrs["placeholder"] = "example@example.com"

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if email.lower() != confirm_email.lower():
            raise forms.ValidationError("Emails do not match!")

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")


