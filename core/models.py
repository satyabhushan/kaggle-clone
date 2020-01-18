import os
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".csv"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(u"Unsupported file extension.")


class Competition(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    brief = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    train_csv = models.FileField(
        upload_to="dataset/", validators=[validate_file_extension]
    )
    test_csv = models.FileField(
        upload_to="dataset/", validators=[validate_file_extension]
    )
    hidden_test_csv = models.FileField(
        upload_to="dataset/", validators=[validate_file_extension]
    )
    train_solution_csv = models.FileField(
        upload_to="dataset/", validators=[validate_file_extension]
    )
    test_solution_csv = models.FileField(
        upload_to="dataset/", validators=[validate_file_extension]
    )
    hidden_test_solution_csv = models.FileField(
        upload_to="dataset/", validators=[validate_file_extension]
    )
    start_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(default=timezone.datetime(2012, 1, 1))
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    competitor = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    container_path = models.CharField(max_length=300, null=True, blank=True)
    container_id = models.CharField(max_length=500, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    submission_csv = models.FileField(
        upload_to="dataset/", validators=[validate_file_extension]
    )
    accuracy = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("competitor", "competition")

