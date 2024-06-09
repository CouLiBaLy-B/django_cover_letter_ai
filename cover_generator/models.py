from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CoverLetter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profil = models.CharField(max_length=5000)
    job_title = models.CharField(max_length=300)
    job_description = models.CharField(max_length=5000)
    generated_content = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title
