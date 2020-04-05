from django.db import models

# Create your models here.
class Page(models.Model):
    name = models.CharField(max_length=255, default="Landing page name")
    owner = models.CharField(max_length=255, default="Page owner")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Referrer(models.Model):
    name = models.CharField(max_length=50, default="Referrer name")
    count = models.IntegerField(default=0)
    page = models.ForeignKey(
        'Page',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
