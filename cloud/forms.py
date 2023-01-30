from django import forms
from .models import File


class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('title', 'file')