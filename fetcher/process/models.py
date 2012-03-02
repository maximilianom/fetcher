from django.db import models

class Error(models.Model):
    url = models.CharField(max_length=100)
    error = models.TextField()

    def __unicode__(self):
        return self.url

    class Meta:
        db_table = "error"
        verbose_name = "error"
        verbose_name_plural = "errors"


# Create your models here.
