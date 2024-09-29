from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class CustomUser(AbstractUser):
    picture = models.ImageField(upload_to='media/')
    def __str__(self):
        return self.username

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sendername=models.ForeignKey(CustomUser, related_name='messages_sender', on_delete=models.CASCADE)
    recipientname=models.ForeignKey(CustomUser, related_name='messages_recipient', on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
# class Sender(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
    
#     def __str__(self):
#         return self.name

# class Recipient(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return self.email