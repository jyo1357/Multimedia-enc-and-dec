import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from .models import EncryptionHistory, FileUpload, AudioUpload, VideoUpload, EncryptedImage, ImageHistory
from .forms import FileUploadForm, AudioUploadForm,VideoUploadForm
from .utils import AESEncryption, encrypt_file, decrypt_file, encrypt_audio,decrypt_audio,encrypt_video,decrypt_video, encrypt_image, decrypt_image_to_base64
from django.conf import settings
from django.contrib import messages

# Landing Page
def landing(request):
    return render(request, 'landing.html')

# Text Encryption
def encrypt_text(request):
    encrypted_text = None
    input_text = None
    if request.method == "POST":
        input_text = request.POST.get('input_text')
        key = request.POST.get('key')
        if not input_text or not key:
            return JsonResponse({'error': 'Input text and key are required.'}, status=400)
        aes = AESEncryption(key)
        encrypted_text = aes.encrypt(input_text)
        EncryptionHistory.objects.create(input_text=input_text, encrypted_text=encrypted_text, decrypted_text='', password=key)
        return render(request, 'encrypt_text.html', {'input_text': input_text, 'encrypted_text': encrypted_text})
    return render(request, 'encrypt_text.html')

# Text Decryption
def decrypt_text(request):
    decrypted_text = None
    encrypted_text = None
    if request.method == "POST":
        encrypted_text = request.POST.get('encrypted_text')
        key = request.POST.get('key')
        if not encrypted_text or not key:
            return JsonResponse({'error': 'Encrypted text and key are required.'}, status=400)
        aes = AESEncryption(key)
        try:
            decrypted_text = aes.decrypt(encrypted_text)
            history_entry = EncryptionHistory.objects.filter(encrypted_text=encrypted_text).first()
            if history_entry:
                history_entry.decrypted_text = decrypted_text
                history_entry.save()
            return render(request, 'encrypt_text.html', {'decrypted_text': decrypted_text, 'encrypted_text': encrypted_text})
        except Exception as e:
            return JsonResponse({'error': f'Decryption failed: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request.'}, status=400)

# Encryption History
def view_history(request):
    history = EncryptionHistory.objects.all()
    return render(request, 'history.html', {'history': history})

# Delete History
def delete_history(request, id):
    entry = get_object_or_404(EncryptionHistory, id=id)
    entry.delete()
    return redirect('history')

def file_operations(request):
    file_instance = None
    decrypted_file_path = None
    encrypted_file_path = None
    error_message = None
    form = FileUploadForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        # Encrypt File
        if action == 'encrypt':
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file_instance = form.save()
                input_path = file_instance.file.path
                password = form.cleaned_data['password']
                encrypted_dir = os.path.join(settings.MEDIA_ROOT, 'encrypted_files')
                os.makedirs(encrypted_dir, exist_ok=True)
                encrypted_path = os.path.join(encrypted_dir, os.path.basename(input_path))
                encrypt_file(input_path, encrypted_path, password)
                file_instance.encrypted_file = encrypted_path
                file_instance.save()
                encrypted_file_path = encrypted_path
            else:
                error_message = "Invalid form input."

        # Decrypt File
        elif action == 'decrypt':
            encrypted_file = request.FILES.get('encrypted_file')
            password = request.POST.get('password')
            if encrypted_file:
                encrypted_dir = os.path.join(settings.MEDIA_ROOT, 'encrypted_files')
                decrypted_dir = os.path.join(settings.MEDIA_ROOT, 'decrypted_files')
                os.makedirs(decrypted_dir, exist_ok=True)
                encrypted_path = os.path.join(encrypted_dir, encrypted_file.name)
                decrypted_path = os.path.join(decrypted_dir, f"decrypted_{encrypted_file.name}")
                with open(encrypted_path, 'wb') as f:
                    for chunk in encrypted_file.chunks():
                        f.write(chunk)
                try:
                    decrypt_file(encrypted_path, decrypted_path, password)
                    decrypted_file_path = decrypted_path
                    file_instance = FileUpload.objects.filter(encrypted_file=encrypted_path).first()
                    if file_instance:
                        file_instance.decrypted_file = decrypted_path
                        file_instance.save()
                except Exception as e:
                    error_message = f"Decryption failed: {str(e)}"
                    os.remove(encrypted_path)
                os.remove(encrypted_path)

    return render(request, 'file_operations.html', {
        'form': form,
        'file_instance': file_instance,
        'decrypted_file_path': decrypted_file_path,
        'encrypted_file_path': encrypted_file_path,
        'error_message': error_message
    })

# File History (List All Files)
def file_history(request):
    files = FileUpload.objects.all()
    return render(request, 'file_history.html', {'files': files})

# File Download
def file_download(request, file_type, file_path):
    if file_type not in ['encrypted', 'decrypted']:
        return HttpResponse("Invalid file file type", status=400)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        return HttpResponse("file File not found", status=404)

# Delete File from History
def delete_file(request, id):
    file_instance = get_object_or_404(FileUpload, id=id)
    file_instance.delete()
    messages.success(request, "file File deleted successfully!")
    return redirect('file_history')

# File Operations (Encrypt and Decrypt)

# def file_operations(request):
#     file_instance = None
#     decrypted_file_path = None
#     encrypted_file_path = None
#     error_message = None
#     form = FileUploadForm()

#     if request.method == 'POST':
#         action = request.POST.get('action')

#         # Encrypt File
#         if action == 'encrypt':
#             form = FileUploadForm(request.POST, request.FILES)
#             if form.is_valid():
#                 file_instance = form.save()
#                 input_path = file_instance.file.path
#                 password = form.cleaned_data['password']
#                 encrypted_dir = os.path.join(settings.MEDIA_ROOT, 'encrypted_files')
#                 os.makedirs(encrypted_dir, exist_ok=True)
#                 encrypted_path = os.path.join(encrypted_dir, os.path.basename(input_path))
#                 encrypt_file(input_path, encrypted_path, password)
#                 file_instance.encrypted_file = encrypted_path
#                 file_instance.save()
#                 encrypted_file_path = encrypted_path
#             else:
#                 error_message = "Invalid form input."

#         # Decrypt File
#         elif action == 'decrypt':
#             encrypted_file = request.FILES.get('encrypted_file')
#             password = request.POST.get('password')
#             if encrypted_file:
#                 encrypted_dir = os.path.join(settings.MEDIA_ROOT, 'encrypted_files')
#                 decrypted_dir = os.path.join(settings.MEDIA_ROOT, 'decrypted_files')
#                 os.makedirs(decrypted_dir, exist_ok=True)
#                 encrypted_path = os.path.join(encrypted_dir, encrypted_file.name)
#                 decrypted_path = os.path.join(decrypted_dir, f"decrypted_{encrypted_file.name}")
#                 with open(encrypted_path, 'wb') as f:
#                     for chunk in encrypted_file.chunks():
#                         f.write(chunk)
#                 try:
#                     decrypt_file(encrypted_path, decrypted_path, password)
#                     decrypted_file_path = decrypted_path
#                     file_instance = FileUpload.objects.filter(encrypted_file=encrypted_path).first()
#                     if file_instance:
#                         file_instance.decrypted_file = decrypted_path
#                         file_instance.save()
#                 except Exception as e:
#                     error_message = f"Decryption failed: {str(e)}"
#                     os.remove(encrypted_path)
#                 os.remove(encrypted_path)

#     return render(request, 'file_operations.html', {
#         'form': form,
#         'file_instance': file_instance,
#         'decrypted_file_path': decrypted_file_path,
#         'encrypted_file_path': encrypted_file_path,
#         'error_message': error_message
#     })

# # File History (List All Files)
# def file_history(request):
#     files = FileUpload.objects.all()
#     for file in files:
#         file.encrypted_status = "Encrypted" if file.encrypted_file else "Not Encrypted"
#         file.decrypted_status = "Decrypted" if file.decrypted_file else "Not Decrypted"
#     return render(request, 'file_history.html', {'files': files})

# # File Download
# def file_download(request, file_type, file_path):
#     if file_type not in ['encrypted', 'decrypted']:
#         return HttpResponse("Invalid file type", status=400)
#     if os.path.exists(file_path):
#         return FileResponse(open(file_path, 'rb'), as_attachment=True)
#     else:
#         return HttpResponse("File not found", status=404)

# # Delete File from History
# def delete_file(request, id):
#     file_instance = get_object_or_404(FileUpload, id=id)
#     file_instance.delete()
#     messages.success(request, "File deleted successfully!")
#     return redirect('file_history')

# Audio Encryption/Decryption Operations
# Audio Encryption/Decryption Operations
# Audio Encryption/Decryption Operations
 # Assumes encryption/decryption utilities exist

def audio_operations(request):
    file_instance = None
    decrypted_audio_path = None
    encrypted_audio_path = None
    error_message = None
    form = AudioUploadForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        # Encrypt File
        if action == 'encrypt':
            form = AudioUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file_instance = form.save()
                input_path = file_instance.file.path
                password = form.cleaned_data['password']
                encrypted_dir = os.path.join(settings.MEDIA_ROOT, 'encrypted_audios')
                os.makedirs(encrypted_dir, exist_ok=True)
                encrypted_path = os.path.join(encrypted_dir, os.path.basename(input_path))
                encrypt_audio(input_path, encrypted_path, password)
                file_instance.encrypted_audio = encrypted_path
                file_instance.save()
                encrypted_audio_path = encrypted_path
            else:
                error_message = "Invalid form input."

        # Decrypt File
        elif action == 'decrypt':
            encrypted_audio = request.FILES.get('encrypted_audio')
            password = request.POST.get('password')
            if encrypted_audio:
                encrypted_dir = os.path.join(settings.MEDIA_ROOT, 'encrypted_audios')
                decrypted_dir = os.path.join(settings.MEDIA_ROOT, 'decrypted_audios')
                os.makedirs(decrypted_dir, exist_ok=True)
                encrypted_path = os.path.join(encrypted_dir, encrypted_audio.name)
                decrypted_path = os.path.join(decrypted_dir, f"decrypted_{encrypted_audio.name}")
                with open(encrypted_path, 'wb') as f:
                    for chunk in encrypted_audio.chunks():
                        f.write(chunk)
                try:
                    decrypt_audio(encrypted_path, decrypted_path, password)
                    decrypted_audio_path = decrypted_path
                    file_instance = AudioUpload.objects.filter(encrypted_audio=encrypted_path).first()
                    if file_instance:
                        file_instance.decrypted_audio = decrypted_path
                        file_instance.save()
                except Exception as e:
                    error_message = f"Decryption failed: {str(e)}"
                    os.remove(encrypted_path)
                os.remove(encrypted_path)

    return render(request, 'audio_operations.html', {
        'form': form,
        'file_instance': file_instance,
        'decrypted_audio_path': decrypted_audio_path,
        'encrypted_audio_path': encrypted_audio_path,
        'error_message': error_message
    })

# File History (List All Files)
def audio_history(request):
    files = AudioUpload.objects.all()
    return render(request, 'audio_history.html', {'files': files})

# File Download
def audio_download(request, file_type, file_path):
    if file_type not in ['encrypted', 'decrypted']:
        return HttpResponse("Invalid Audio file type", status=400)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        return HttpResponse("Audio File not found", status=404)

# Delete File from History
def delete_audio(request, id):
    file_instance = get_object_or_404(AudioUpload, id=id)
    file_instance.delete()
    messages.success(request, "Audio File deleted successfully!")
    return redirect('audio_history')


# image(encryption and decryption)

# def upload_image(request):
#     if request.method == 'POST':
#         image = request.FILES['image']
#         key = request.POST['key']

#         # Save original image
#         obj = EncryptedImage(original_image=image, key=key)
#         obj.save()

#         # Encrypt image
#         original_path = os.path.join(settings.MEDIA_ROOT, obj.original_image.name)
#         encrypted_path = encrypt_image(original_path, key)
#         obj.encrypted_image.name = encrypted_path.replace(settings.MEDIA_ROOT + '/', '')
#         obj.save()

#         return redirect('view_image', pk=obj.id)

#     return render(request, 'upload_image.html')


# from .utils import decrypt_image_to_base64

# def view_image(request, pk):
#     obj = EncryptedImage.objects.get(pk=pk)

#     decrypted_image_base64 = None

#     if request.method == 'POST':
#         key = request.POST.get('key', '')

#         if key:
#             encrypted_path = os.path.join(settings.MEDIA_ROOT, obj.encrypted_image.name)
#             decrypted_image_base64 = decrypt_image_to_base64(encrypted_path, key)

#     return render(request, 'view_image.html', {
#         'image': obj,
#         'decrypted_image_base64': decrypted_image_base64,  # Base64 image for display
#     })

# # views.py

# def image_history(request):
#     # Fetch all ImageHistory records, ordered by the most recent first
#     history = ImageHistory.objects.all()  # Assuming 'created_at' field exists
#     return render(request, 'image_history.html', {'history': history})

# def delete_image(request, id):
#     history = get_object_or_404(ImageHistory, id=id)
#     history.delete()
#     return redirect('image_history')
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
        key = request.POST['key']
        
        # Save original image
        obj = EncryptedImage(original_image=image, key=key)
        obj.save()

        # Encrypt image
        original_path = os.path.join(settings.MEDIA_ROOT, obj.original_image.name)
        encrypted_path = encrypt_image(original_path, key)
        obj.encrypted_image.name = encrypted_path.replace(settings.MEDIA_ROOT + '/', '')
        obj.save()

        return redirect('view_image', pk=obj.id)

    return render(request, 'upload_image.html')


from .utils import decrypt_image_to_base64
from base64 import b64decode
def view_image(request, pk):
    obj = EncryptedImage.objects.get(pk=pk)

    decrypted_image_base64 = None

    if request.method == 'POST':
        key = request.POST.get('key', '')

        if key:
            encrypted_path = os.path.join(settings.MEDIA_ROOT, obj.encrypted_image.name)
            decrypted_image_base64 = decrypt_image_to_base64(encrypted_path, key)
            decrypted_image_path = f"{os.path.splitext(encrypted_path)[0]}_decrypted.png"

            decrypted_image = ImageHistory(
                original_image=obj.original_image,
                decrypted_image_base64=decrypted_image_path,
                key=key
            )
            decrypted_image.save()
            encrypted_image_url = obj.encrypted_image.url  # Get the encrypted image URL
            decrypted_image.encrypted_image = encrypted_image_url  # Save the encrypted image URL in history
            decrypted_image.save()
    return render(request, 'view_image.html', {
        'image': obj,
        'decrypted_image_base64': decrypted_image_base64,  # Base64 image for display
    })

# views.py

def image_history(request):
    # Fetch all ImageHistory records, ordered by the most recent first
    history = ImageHistory.objects.all()  # Assuming 'created_at' field exists
    return render(request, 'image_history.html', {'history': history})

def delete_image_history(request, id):
    history_entry = get_object_or_404(ImageHistory, id=id)
    history_entry.delete()
    return redirect('image_history') 

def video_operations(request):
    file_instance = None
    decrypted_video_path = None
    encrypted_video_path = None
    error_message = None
    form = VideoUploadForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        # Encrypt File
        if action == 'encrypt':
            form = VideoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file_instance = form.save()
                input_path = file_instance.file.path
                password = form.cleaned_data['password']
                encrypted_dir = os.path.join(settings.MEDIA_ROOT, 'encrypted_videos')
                os.makedirs(encrypted_dir, exist_ok=True)
                encrypted_path = os.path.join(encrypted_dir, os.path.basename(input_path))
                encrypt_video(input_path, encrypted_path, password)
                file_instance.encrypted_video = encrypted_path
                file_instance.save()
                encrypted_video_path = encrypted_path
            else:
                error_message = "Invalid form of input."

        # Decrypt File
        elif action == 'decrypt':
            encrypted_video = request.FILES.get('encrypted_video')
            password = request.POST.get('password')
            if encrypted_video:
                encrypted_dir = os.path.join(settings.MEDIA_ROOT, 'encrypted_videos')
                decrypted_dir = os.path.join(settings.MEDIA_ROOT, 'decrypted_videos')
                os.makedirs(decrypted_dir, exist_ok=True)
                encrypted_path = os.path.join(encrypted_dir, encrypted_video.name)
                decrypted_path = os.path.join(decrypted_dir, f"decrypted_{encrypted_video.name}")
                with open(encrypted_path, 'wb') as f:
                    for chunk in encrypted_video.chunks():
                        f.write(chunk)
                try:
                    decrypt_video(encrypted_path, decrypted_path, password)
                    decrypted_video_path = decrypted_path
                    file_instance = VideoUpload.objects.filter(encrypted_video=encrypted_path).first()
                    if file_instance:
                        file_instance.decrypted_video = decrypted_path
                        file_instance.save()
                except Exception as e:
                    error_message = f"Decryption failed: {str(e)}"
                    os.remove(encrypted_path)
                os.remove(encrypted_path)

    return render(request, 'video_operations.html', {
        'form': form,
        'file_instance': file_instance,
        'decrypted_video_path': decrypted_video_path,
        'encrypted_video_path': encrypted_video_path,
        'error_message': error_message
    })

# File History (List All Files)
def video_history(request):
    files = VideoUpload.objects.all()
    return render(request, 'video_history.html', {'files': files})

# File Download
def video_download(request, file_type, file_path):
    if file_type not in ['encrypted', 'decrypted']:
        return HttpResponse("Invalid Video file type", status=400)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        return HttpResponse("Video File not found", status=404)

# Delete File from History
def delete_video(request, id):
    file_instance = get_object_or_404(VideoUpload, id=id)
    file_instance.delete()
    messages.success(request, "video File deleted successfully!")
    return redirect('video_history')


