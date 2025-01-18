from django.contrib.auth.models import User
from django.db import models

class Contract(models.Model):    
    STATUS_CHOICES = [
        ('created', 'created'),
        ('sent', 'sent'),
        ('completed', 'completed'),
        ('signed', 'signed'),
        ('failed', 'failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    envelope_id = models.CharField(max_length=255, blank=True, null=True)  
    recipient_email = models.EmailField()  
    recipient_name = models.CharField(max_length=255)  
    contract_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  
    signed_by_user = models.BooleanField(default=False) 
    signed_by_recipient = models.BooleanField(default=False) 
    contract_name = models.CharField(max_length=255, null=True, blank=True)  
    name_of_other_signer = models.CharField(max_length=100)  
    email_of_other_signer = models.EmailField(null=True, blank=True) 
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')  
    is_signed = models.BooleanField(default=False)

    def __str__(self):
        return f'Contract {self.envelope_id} for {self.recipient_email}'
    
    def is_complete(self):
        return self.status == 'completed' and self.signed_by_user and self.signed_by_recipient

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'contract'
        verbose_name_plural = 'contracts'
