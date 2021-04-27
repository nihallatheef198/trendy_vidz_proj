from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class group(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('grp_dtl', kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class video(models.Model):
    title = models.CharField(max_length=50)
    url =models.URLField()
    u_tube_id = models.CharField(max_length=50)
    group = models.ForeignKey(group, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
