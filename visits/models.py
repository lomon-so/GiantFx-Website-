from django.db import models

class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=2, blank=True)
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} visited {self.path} at {self.timestamp}"
