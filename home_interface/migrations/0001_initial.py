# Generated by Django 4.2.6 on 2023-10-24 00:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Competition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="competition_images/"
                    ),
                ),
                ("start_regi", models.DateField()),
                ("end_regi", models.DateField()),
                ("start_compt", models.DateField()),
                ("url", models.URLField(blank=True, null=True)),
                ("number", models.PositiveIntegerField(blank=True, null=True)),
                ("intro", models.TextField()),
                (
                    "category",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Category 1"),
                            (2, "Category 2"),
                            (3, "Category 3"),
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_name", models.CharField(max_length=15)),
                (
                    "user_id",
                    models.IntegerField(
                        unique=True,
                        validators=[
                            django.core.validators.MaxValueValidator(20),
                            django.core.validators.MinValueValidator(1),
                        ],
                    ),
                ),
                ("user_password", models.CharField(max_length=20)),
                (
                    "profile",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_pictures/"
                    ),
                ),
                ("bio", models.TextField(blank=True, max_length=500, null=True)),
                ("major", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "competition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="home_interface.competition",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_teams",
                        to="home_interface.user",
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        related_name="joined_teams", to="home_interface.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Discussion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("discuss_time", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discussions",
                        to="home_interface.user",
                    ),
                ),
            ],
        ),
    ]
