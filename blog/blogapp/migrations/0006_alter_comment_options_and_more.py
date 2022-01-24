# Generated by Django 4.0 on 2022-01-24 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_post_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('date_added',)},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='date_added',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='active',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='updated',
        ),
    ]