from django.db import models
from datetime import datetime

# Model for storing encryption history of text-based data
class EncryptionHistory(models.Model):
    input_text = models.TextField()  # Original input text
    encrypted_text = models.TextField()  # Encrypted text
    decrypted_text = models.TextField(blank=True, null=True)  # Decrypted text (nullable)
    password = models.CharField(max_length=100)  # Encryption key
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of encryption

    def __str__(self):
        return f"Input: {self.input_text[:20]}... - {self.timestamp}"

# Model for storing file uploads and their encryption/decryption states
class FileUpload(models.Model):
    file = models.FileField(upload_to='uploaded_files/')  # Original file uploaded by the user
    password = models.CharField(max_length=100, default='default_password')  # Password for encryption/decryption
    uploaded_at = models.DateTimeField(auto_now_add=True)  # DateTime of file upload

    # Fields for storing encrypted and decrypted versions of the file
    encrypted_file = models.FileField(upload_to='encrypted_files/', null=True, blank=True)
    decrypted_file = models.FileField(upload_to='decrypted_files/', null=True, blank=True)
    
    def __str__(self):
        return f"File {self.id} - {self.file.name}"

from django.db import models

class AudioUpload(models.Model):
    file = models.FileField(upload_to='uploaded_audios/', verbose_name="Original Audio File")  # File upload field
    password = models.CharField(max_length=100, default='default_password', verbose_name="Password for Encryption/Decryption")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Upload Timestamp")
    encrypted_audio = models.FileField(upload_to='encrypted_audios/', null=True, blank=True, verbose_name="Encrypted Audio File")
    decrypted_audio = models.FileField(upload_to='decrypted_audios/', null=True, blank=True, verbose_name="Decrypted Audio File")

    @property
    def encrypted_status(self):
        """Returns the encryption status of the file."""
        return "Encrypted" if self.encrypted_audio else "Not Encrypted"

    @property
    def decrypted_status(self):
        """Returns the decryption status of the file."""
        return "Decrypted" if self.decrypted_audio else "Not Decrypted"

    def __str__(self):
        """String representation for the model."""
        return f"Audio {self.id} - {self.file.name}"
  # Updated 'audio' to 'file'

# Model for storing encrypted image data
class EncryptedImage(models.Model):
    original_image = models.ImageField(upload_to='original_images/')  # Original image uploaded
    encrypted_image = models.ImageField(upload_to='encrypted_images/', blank=True, null=True)  # Encrypted image
    key = models.CharField(max_length=255)  # Store encryption key for the image

    def __str__(self):
        return f"Encrypted Image: {self.original_image.name}"

# Model for storing image history, including decrypted versions
class ImageHistory(models.Model):
    original_image = models.ImageField(upload_to='original_images/', null=True, blank=True)  # Original image uploaded
    #encrypted_image = models.ImageField(upload_to='encrypted_images/',null=True, blank=True)
    decrypted_image_base64 = models.ImageField(upload_to='decrypted_images/', null=True, blank=True)  # Decrypted image
    key = models.CharField(max_length=256, blank=True, null=True) # Encryption key used for this image

    def __str__(self):
        return f"Image {self.id} - {self.date_uploaded}"
    



# # # Model for storing encrypted image data
# class EncryptedImage(models.Model):
#     original_image = models.ImageField(upload_to='original_images/')  # Original image uploaded
#     encrypted_image = models.ImageField(upload_to='encrypted_images/', blank=True, null=True)  # Encrypted image
#     key = models.CharField(max_length=255)  # Store encryption key for the image

#     def __str__(self):
#         return f"Encrypted Image: {self.original_image.name}"

# # Model for storing image history, including decrypted versions
# class ImageHistory(models.Model):
#     original_image = models.ImageField(upload_to='original_images/')  # Original image uploaded
#     decrypted_image = models.ImageField(upload_to='decrypted_images/', null=True, blank=True)  # Decrypted image
#     password = models.CharField(max_length=255,null=True, blank=True)  # Encryption key used for this image
#     # 2 # DateTime when the image was uploaded

#     def __str__(self):
#         return f"Image {self.id} - {self.date_uploaded}"




class VideoUpload(models.Model):
    file = models.FileField(upload_to='uploaded_videos/', verbose_name="Original Video File")  # File upload field
    password = models.CharField(max_length=100, default='default_password', verbose_name="Password for Encryption/Decryption")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Upload Timestamp")
    encrypted_video = models.FileField(upload_to='encrypted_videos/', null=True, blank=True, verbose_name="Encrypted Video File")
    decrypted_video = models.FileField(upload_to='decrypted_videos/', null=True, blank=True, verbose_name="Decrypted Video File")

    @property
    def encrypted_status(self):
        """Returns the encryption status of the file."""
        return "Encrypted" if self.encrypted_video else "Not Encrypted"

    @property
    def decrypted_status(self):
        """Returns the decryption status of the file."""
        return "Decrypted" if self.decrypted_video else "Not Decrypted"

    def __str__(self):
        """String representation for the model."""
        return f"Video {self.id} - {self.file.name}"