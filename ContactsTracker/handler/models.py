from django.db import models

# Create your models here.
class Contact(models.Model):
    # class ContactType(models.TextChoices):
    #     primary = 'primary'
    #     secondary = 'secondary'
        
    phoneNumber = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    linkedId = models.IntegerField(null=True, blank=True)
    linkPrecedence = models.CharField(max_length=20, default='primary')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'Contact'