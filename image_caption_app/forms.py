from django import forms


class MultipleImageUploadForm(forms.Form):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            "multiple": True,
            "accept": "images/*"
        })
    )




