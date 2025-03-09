# Generated by Django 5.1.3 on 2024-12-26 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encryption', '0029_alter_fileupload_decrypted_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='decrypted_file',
            field=models.FileField(blank=True, null=True, upload_to='decrypted_files/', verbose_name='Decrypted file File'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='encrypted_file',
            field=models.FileField(blank=True, null=True, upload_to='encrypted_files/', verbose_name='Encrypted file File'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(upload_to='uploaded_files/', verbose_name='Original file File'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='password',
            field=models.CharField(default='default_password', max_length=100, verbose_name='Password for Encryption/Decryption'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Upload Timestamp'),
        ),
    ]
