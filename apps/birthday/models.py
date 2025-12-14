from django.db import models


class BirthdayPageSettings(models.Model):
    """Birthday Page Settings"""
    # Breadcrumb
    breadcrumb_title = models.CharField(max_length=200, default="Doğum Günü Şənlikləri", blank=True, null=True, verbose_name="Breadcrumb Başlıq")
    breadcrumb_description = models.TextField(max_length=500, default="Uşaqlarınızın Doğum Gününü Alisa Club-da Unudulmaz Edin!", blank=True, null=True, verbose_name="Breadcrumb Təsvir")
    breadcrumb_image = models.ImageField(upload_to='birthday/breadcrumb/', blank=True, null=True, verbose_name="Breadcrumb Arxa Fon", help_text='Tövsiyə olunan ölçü: 1920x520 piksel')
    
    # Hero Section
    hero_subtitle = models.CharField(max_length=200, default="🎉 Uşaqlarınız üçün ən xoş günlər", blank=True, null=True, verbose_name="Hero Alt Başlıq")
    hero_title = models.CharField(max_length=300, default="Doğum Gününü Alisa Club-da Unudulmaz Edin!", blank=True, null=True, verbose_name="Hero Başlıq")
    hero_description = models.TextField(blank=True, null=True, verbose_name="Hero Təsvir")
    hero_image = models.ImageField(upload_to='birthday/hero/', blank=True, null=True, verbose_name="Hero Şəkil", help_text='Tövsiyə olunan ölçü: 543x339 piksel')
    hero_button_text = models.CharField(max_length=50, default="Rezervasiya Et", blank=True, null=True, verbose_name="Hero Düymə Mətni")
    hero_button_url = models.CharField(max_length=200, default="#contact-section", blank=True, null=True, verbose_name="Hero Düymə URL")
    
    # Gallery Section
    gallery_subtitle = models.CharField(max_length=200, default="📷 Qalereya", blank=True, null=True, verbose_name="Qalereyası Alt Başlıq")
    gallery_title = models.CharField(max_length=300, default="Keçmiş Şənliklərdən Görüntülər", blank=True, null=True, verbose_name="Qalereyası Başlıq")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Doğum Günü Səhifə Parametrləri"
        verbose_name_plural = "Doğum Günü Səhifə Parametrləri"

    def __str__(self):
        return "Doğum Günü Səhifə Parametrləri"

    def save(self, *args, **kwargs):
        if not self.pk and BirthdayPageSettings.objects.exists():
            raise ValueError('Yalnız bir Doğum Günü Səhifə Parametrləri yarada bilərsiniz.')
        return super().save(*args, **kwargs)


class BirthdayGallery(models.Model):
    """Birthday Gallery Images"""
    image = models.ImageField(upload_to='birthday/gallery/', blank=True, null=True, verbose_name="Şəkil", help_text='Tövsiyə olunan ölçü: 310x250 piksel')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Başlıq")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")

    class Meta:
        verbose_name = "Doğum Günü Qalereyası"
        verbose_name_plural = "Doğum Günü Qalereyaları"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or f"Şəkil {self.id}"


class BirthdayReservation(models.Model):
    """Birthday Reservation Form Submissions"""
    child_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Uşağın Adı")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Uşağın Doğum Tarixi")
    event_date = models.DateField(blank=True, null=True, verbose_name="Şənlik Tarixi", help_text="Doğum günü şənliyinin keçiriləcəyi tarix")
    parent_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Valideynin Adı")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    participants = models.PositiveIntegerField(blank=True, null=True, verbose_name="İştirakçı Sayı")
    notes = models.TextField(blank=True, null=True, verbose_name="Əlavə Qeydlər", help_text="Müştərinin xüsusi istəkləri")
    subscribe_to_events = models.BooleanField(default=False, verbose_name="Tədbirlərə Abunə")
    
    # Admin fields
    is_read = models.BooleanField(default=False, verbose_name="Oxundu")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Admin Qeydləri")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Göndərilmə Tarixi")

    class Meta:
        verbose_name = "Doğum Günü Rezervasiyası"
        verbose_name_plural = "Doğum Günü Rezervasiyaları"
        ordering = ['-created_at']

    def __str__(self):
        event_date_str = self.event_date.strftime('%d.%m.%Y') if self.event_date else 'Tarix yoxdur'
        return f"{self.child_name} - {event_date_str}"
