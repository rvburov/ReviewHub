# Generated by Django 3.2 on 2023-11-27 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_username'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_name_email',
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('username', 'email'), name='unique_username_email'),
        ),
    ]
