from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),  # Homepage with boxes
    path('encrypt/', views.encrypt_text, name='encrypt_text'),  # Text encryption page
    path('decrypt/', views.decrypt_text, name='decrypt_text'),  # Text decryption page
    path('history/', views.view_history, name='history'),  # Encryption/Decryption history page
    path('delete_history/<int:id>/', views.delete_history, name='delete_history'),  # Delete history by ID
    
    path('file_operations/', views.file_operations, name='file_operations'),  # File encryption/decryption operations
    path('file_history/', views.file_history, name='file_history'),  # File encryption/decryption history page
    path('file_download/<str:file_type>/<path:file_path>/', views.file_download, name='file_download'),  # File download
    path('delete_file/<int:id>/', views.delete_file, name='delete_file'),  # Delete file from history

    path('audio_operations/', views.audio_operations, name='audio_operations'),  # Audio encryption/decryption operations
    path('audio_history/', views.audio_history, name='audio_history'),  # Audio encryption/decryption history page
    path('audio_download/<str:file_type>/<str:file_path>/', views.audio_download, name='audio_download'),
    path('delete_audio/<int:id>/', views.delete_audio, name='delete_audio'),  # Delete audio from history

    
    path('upload_image/', views.upload_image, name='upload_image'),  # Image upload page
    path('view_image/<int:pk>/', views.view_image, name='view_image'),  # View image details
    path('image_history/', views.image_history, name='image_history'),  # Image encryption history page
    #path('delete_history_item/<int:pk>/', views.delete_history_item, name='delete_history_item'),
    path('delete_image_history/<int:id>/', views.delete_image_history, name='delete_image_history'),

    path('video_operations/', views.video_operations, name='video_operations'),  # Audio encryption/decryption operations
    path('video_history/', views.video_history, name='video_history'),  # Audio encryption/decryption history page
    path('video_download/<str:file_type>/<str:file_path>/', views.video_download, name='video_download'),
    path('delete_video/<int:id>/', views.delete_video, name='delete_video'),  # Delete audio from history
]

