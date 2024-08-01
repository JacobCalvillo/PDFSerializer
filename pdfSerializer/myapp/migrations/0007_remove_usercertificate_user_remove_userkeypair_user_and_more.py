# Generated by Django 5.0.7 on 2024-08-01 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_userkeypair_private_key_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercertificate',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userkeypair',
            name='user',
        ),
        migrations.RemoveField(
            model_name='signeddocument',
            name='signed_file_url',
        ),
        migrations.AddField(
            model_name='signeddocument',
            name='encrypted_file',
            field=models.BinaryField(default=b''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DigitalSign',
        ),
        migrations.DeleteModel(
            name='UserCertificate',
        ),
        migrations.DeleteModel(
            name='UserKeyPair',
        ),
    ]
