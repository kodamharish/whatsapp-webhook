from django.db import models

# Create your models here.
# webhook/models.py

from django.db import models

class Message(models.Model):
    phone_number = models.CharField(max_length=20)
    message_body = models.TextField()
    response_body = models.TextField(null=True, blank=True)  # New field to save the response
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.phone_number} at {self.timestamp}"
