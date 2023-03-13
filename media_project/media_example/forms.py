from django import forms
from .models import ExampleModel


class UploadForm(forms.ModelForm):  # forms.Form
    # file_upload = forms.FileField()
    # file_upload = forms.ImageField()
    # image_upload = forms.ImageField()
    # file_upload = forms.FileField()
    class Meta:
        model = ExampleModel
        fields = '__all__'
