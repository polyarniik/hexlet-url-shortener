from django import forms


class URLForm(forms.Form):
    url = forms.URLField(label="URL")
