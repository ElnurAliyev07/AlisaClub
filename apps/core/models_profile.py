from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class ParentProfile(models.Model):
    """Valideyn profili"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    phone = models.CharField(max_length=20, verbose_name="Telefon", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qeydiyyat tarixi")
    
    class Meta:
        verbose_name = "Valideyn Profili"
        verbose_name_plural = "Valideyn Profilləri"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Profil"
    
    def get_medal_count(self):
        """Bütün uşaqların medallarının sayı"""
        return Medal.objects.filter(child__parent=self).count()
    
    def get_status(self):
        """Medal sayına görə status"""
        count = self.get_medal_count()
        if count >= 10:
            return "Qızıl üzv"
        elif count >= 6:
            return "Gümüş üzv"
        elif count >= 3:
            return "Aktiv üzv"
        return "Yeni üzv"


class Child(models.Model):
    """Uşaq məlumatı"""
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100, verbose_name="Uşağın adı")
    birth_date = models.DateField(verbose_name="Doğum tarixi")
    photo = models.ImageField(upload_to='children/', blank=True, null=True, verbose_name="Şəkil", help_text="Uşağın profil şəkli")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Uşaq"
        verbose_name_plural = "Uşaqlar"
        ordering = ['-birth_date']
    
    def __str__(self):
        return f"{self.name} ({self.get_age()} yaş)"
    
    def get_age(self):
        """Uşağın yaşını hesabla"""
        today = timezone.now().date()
        age = today.year - self.birth_date.year
        if today.month < self.birth_date.month or (today.month == self.birth_date.month and today.day < self.birth_date.day):
            age -= 1
        return age
    
    def is_birthday_soon(self, days=14):
        """Doğum günü yaxınlaşır?"""
        today = timezone.now().date()
        birthday_this_year = self.birth_date.replace(year=today.year)
        
        if birthday_this_year < today:
            birthday_this_year = self.birth_date.replace(year=today.year + 1)
        
        days_until = (birthday_this_year - today).days
        return 0 <= days_until <= days


class MedalType(models.Model):
    """Medal növləri"""
    name = models.CharField(max_length=100, verbose_name="Medal adı")
    icon = models.CharField(max_length=10, verbose_name="Emoji/İkon", default="🏆")
    description = models.TextField(verbose_name="Açıqlama", blank=True)
    
    class Meta:
        verbose_name = "Medal Növü"
        verbose_name_plural = "Medal Növləri"
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class Medal(models.Model):
    """Uşağın qazandığı medallar - Yalnız admin tərəfindən verilir"""
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='medals', verbose_name="Uşaq")
    medal_type = models.ForeignKey(MedalType, on_delete=models.CASCADE, verbose_name="Medal növü")
    event_name = models.CharField(max_length=200, verbose_name="Tədbir adı", blank=True, null=True)
    event_date = models.DateField(verbose_name="Tədbir tarixi", blank=True, null=True)
    reason = models.TextField(verbose_name="Qazanma səbəbi", blank=True)
    show_on_homepage = models.BooleanField(default=False, verbose_name="Ana səhifədə göstər", help_text="Seçilsə, bu medal ana səhifədə göstəriləcək")
    awarded_at = models.DateTimeField(auto_now_add=True, verbose_name="Verilmə tarixi")
    
    class Meta:
        verbose_name = "Medal"
        verbose_name_plural = "Medallar"
        ordering = ['-awarded_at']
    
    def __str__(self):
        return f"{self.child.name} - {self.medal_type.name}"
    
    def get_child_photo(self):
        """Uşağın şəkli varsa qaytarır"""
        # Əgər Child modelində photo sahəsi varsa
        return getattr(self.child, 'photo', None)


class Discount(models.Model):
    """Kampaniyalar və Endirimlər - Hamıya göstərilir"""
    title = models.CharField(max_length=200, verbose_name="Kampaniya başlığı")
    description = models.TextField(verbose_name="Açıqlama")
    image = models.ImageField(upload_to='campaigns/', blank=True, null=True, verbose_name="Kampaniya şəkli", help_text="Tövsiyə olunan ölçü: 400x300 piksel")
    discount_percent = models.IntegerField(verbose_name="Endirim faizi", default=10, help_text="Məsələn: 20 (20% endirim)")
    code = models.CharField(max_length=50, verbose_name="Endirim kodu", blank=True, help_text="Məsələn: SUMMER2024")
    valid_from = models.DateField(verbose_name="Başlama tarixi")
    valid_until = models.DateField(verbose_name="Bitmə tarixi")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    show_on_homepage = models.BooleanField(default=False, verbose_name="Ana səhifədə göstər")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma tarixi", null=True, blank=True)
    
    class Meta:
        verbose_name = "Kampaniya"
        verbose_name_plural = "Kampaniyalar"
        ordering = ['-valid_from']
    
    def __str__(self):
        return f"{self.title} - {self.discount_percent}%"
    
    def is_valid(self):
        """Kampaniya hələ etibarlıdır?"""
        today = timezone.now().date()
        return self.is_active and self.valid_from <= today <= self.valid_until
    
    def get_days_left(self):
        """Kampaniyanın bitməsinə neçə gün qalıb"""
        today = timezone.now().date()
        if self.valid_until >= today:
            return (self.valid_until - today).days
        return 0
