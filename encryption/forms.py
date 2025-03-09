from django import forms # type: ignore
from .models import FileUpload, AudioUpload, VideoUpload

# Form for text encryption
class TextEncryptionForm(forms.Form):
    input_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), label="Enter Text")
    key = forms.CharField(widget=forms.PasswordInput, label="Encryption Key")

# Form for file upload (encrypted/decrypted files)
class FileUploadForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}), required=True, label="Password for Encryption")

    class Meta:
        model = FileUpload
        fields = ('file', 'password')

# Form for audio upload (encrypted/decrypted audio files)
class AudioUploadForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}), required=True, label="Password for Encryption")

    class Meta:
        model = AudioUpload
        fields = ('file', 'password')

class VideoUploadForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}), required=True, label="Password for Encryption")

    class Meta:
        model = VideoUpload
        fields = ('file', 'password')