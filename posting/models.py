from django.db import models

class Posting(models.Model):
    name       = models.CharField(max_length=40)
    password   = models.CharField(max_length=500)
    title      = models.CharField(max_length=100)
    contents   = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posting'