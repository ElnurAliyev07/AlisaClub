from django.db import models


class Contact(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='contact/', blank=True, null=True, help_text='Tövsiyə olunan ölçü: 1920x520 piksel')

    class Meta:
        verbose_name = "Əlaqə"
        verbose_name_plural = "Əlaqə Bölməsi"


class ContactMessage(models.Model):
    """Contact Form Messages"""
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ad")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Soyad")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    message = models.TextField(blank=True, null=True, verbose_name="Mesaj")
    
    # Admin fields
    is_read = models.BooleanField(default=False, verbose_name="Oxundu")
    notes = models.TextField(blank=True, null=True, verbose_name="Admin Qeydləri")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Göndərilmə Tarixi")

    class Meta:
        verbose_name = "Əlaqə Mesajı"
        verbose_name_plural = "Əlaqə Mesajları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.created_at.strftime('%d.%m.%Y')}"