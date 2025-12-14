from django.db import models
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Hero(models.Model):
    event_title = models.TextField(max_length=255, blank=True, null=True, verbose_name='Event Title')
    event_description = models.TextField(blank=True, null=True, verbose_name='Event Description')
    
    image = models.ImageField(
        upload_to='hero/', 
        blank=True, 
        null=True, 
        verbose_name='Şəkil',
        help_text='Tövsiyə olunan ölçü: 708x710 piksel'
    )

    class Meta:
        verbose_name = 'Hero'
        verbose_name_plural = 'Hero'
    
    # def save(self, *args, **kwargs):
    #     if self.image:
    #         # Şəkli aç
    #         img = Image.open(self.image)
            
    #         # Orijinal fayl adı və formatı
    #         original_name = self.image.name
    #         original_format = img.format or 'PNG'
    #         file_extension = original_name.split('.')[-1].lower()
            
    #         # Menecer tərəfindən təyin edilmiş ölçü
    #         target_width = self.image_width or 1920
    #         target_height = self.image_height or 1080
            
    #         # Şəkli DƏQİQ ölçüyə gətir (aspect ratio dəyişir)
    #         img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
    #         # Şəkli yaddaşa yaz
    #         output = BytesIO()
            
    #         # PNG formatında saxla (şəffaflıq üçün)
    #         if file_extension == 'png' or img.mode == 'RGBA':
    #             img.save(output, format='PNG', optimize=True)
    #             content_type = 'image/png'
    #             file_ext = 'png'
    #         else:
    #             # JPEG üçün RGB-yə çevir
    #             if img.mode in ('RGBA', 'LA', 'P'):
    #                 background = Image.new('RGB', img.size, (255, 255, 255))
    #                 background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
    #                 img = background
    #             img.save(output, format='JPEG', quality=85, optimize=True)
    #             content_type = 'image/jpeg'
    #             file_ext = 'jpg'
            
    #         output.seek(0)
            
    #         # Yeni faylı yarat
    #         self.image = InMemoryUploadedFile(
    #             output, 
    #             'ImageField', 
    #             f"{original_name.split('.')[0]}.{file_ext}",
    #             content_type,
    #             sys.getsizeof(output), 
    #             None
    #         )
        
    #     super().save(*args, **kwargs)


class About(models.Model):
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name='Alt başlıq')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Başlıq')
    description = models.TextField(blank=True, null=True, verbose_name='Əsas mətn')
    
    # 4 şəkil sahəsi
    image_1 = models.ImageField(
        upload_to='about/', 
        blank=True, 
        null=True, 
        verbose_name='Şəkil 1 (Böyük)',
        help_text='Tövsiyə olunan ölçü: 281x274 piksel'
    )
    image_2 = models.ImageField(
        upload_to='about/', 
        blank=True, 
        null=True, 
        verbose_name='Şəkil 2 (Kiçik üst)',
        help_text='Tövsiyə olunan ölçü: 281x274 piksel'
    )
    image_3 = models.ImageField(
        upload_to='about/', 
        blank=True, 
        null=True, 
        verbose_name='Şəkil 3 (Kiçik orta)',
        help_text='Tövsiyə olunan ölçü: 281x274 piksel'
    )
    image_4 = models.ImageField(
        upload_to='about/', 
        blank=True, 
        null=True, 
        verbose_name='Şəkil 4 (Kiçik alt)',
        help_text='Tövsiyə olunan ölçü: 281x274 piksel'
    )
    
    # Statistika sahələri
    stat_1_value = models.CharField(max_length=20, default='75', blank=True, null=True, verbose_name='Statistika 1 - Dəyər')
    stat_1_text = models.CharField(max_length=100, default='Açıq Hava Fəaliyyətləri', blank=True, null=True, verbose_name='Statistika 1 - Mətn')
    
    stat_2_value = models.CharField(max_length=20, default='23', blank=True, null=True, verbose_name='Statistika 2 - Dəyər')
    stat_2_text = models.CharField(max_length=100, default='Sevgi Dolu Müəllimlər', blank=True, null=True, verbose_name='Statistika 2 - Mətn')
    

    class Meta:
        verbose_name = 'Haqqımızda səhifəsi'
        verbose_name_plural = 'Haqqımızda səhifəsi'
        
    def __str__(self):
        return self.title or "Haqqımızda"

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         # Şəkli aç
    #         img = Image.open(self.image)
            
    #         # Orijinal fayl adı və formatı
    #         original_name = self.image.name
    #         original_format = img.format or 'PNG'
    #         file_extension = original_name.split('.')[-1].lower()
            
    #         # Menecer tərəfindən təyin edilmiş ölçü
    #         target_width = self.image_width or 590
    #         target_height = self.image_height or 590
            
    #         # Şəkli DƏQİQ ölçüyə gətir (aspect ratio dəyişir)
    #         img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
    #         # Şəkli yaddaşa yaz
    #         output = BytesIO()
            
    #         # PNG formatında saxla (şəffaflıq üçün)
    #         if file_extension == 'png' or img.mode == 'RGBA':
    #             img.save(output, format='PNG', optimize=True)
    #             content_type = 'image/png'
    #             file_ext = 'png'
    #         else:
    #             # JPEG üçün RGB-yə çevir
    #             if img.mode in ('RGBA', 'LA', 'P'):
    #                 background = Image.new('RGB', img.size, (255, 255, 255))
    #                 background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
    #                 img = background
    #             img.save(output, format='JPEG', quality=85, optimize=True)
    #             content_type = 'image/jpeg'
    #             file_ext = 'jpg'
            
    #         output.seek(0)
            
    #         # Yeni faylı yarat
    #         self.image = InMemoryUploadedFile(
    #             output, 
    #             'ImageField', 
    #             f"{original_name.split('.')[0]}.{file_ext}",
    #             content_type,
    #             sys.getsizeof(output), 
    #             None
    #         )
        
    #     super().save(*args, **kwargs)

class SessionTime(models.Model):
    PERIOD_CHOICES = [
        ('morning', 'Səhər'),
        ('afternoon', 'Günorta'),
        ('evening', 'Axşam'),
    ]
    
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='session_times', blank=True, null=True)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, blank=True, null=True, verbose_name='Dövr')
    time_range = models.CharField(max_length=50, blank=True, null=True, verbose_name='Vaxt aralığı')
    
    class Meta:
        verbose_name = 'Dərs vaxtı'
        verbose_name_plural = 'Dərs vaxtları'
        ordering = ['period']
    
    def __str__(self):
        return f"{self.get_period_display()}: {self.time_range}"


class WhyChooseUs(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Başlıq', default='Niyə Biz?')
    subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Alt başlıq', default='Əsas Dəyərlərimiz')
    description = models.TextField(blank=True, null=True, verbose_name='Açıqlama', help_text='Bu hissə "Niyə Biz?" bölməsinin əsas mətnidir')
    is_active = models.BooleanField(default=True, verbose_name='Aktiv')

    class Meta:
        verbose_name = 'Niyə Biz? Səhifəsi'
        verbose_name_plural = 'Niyə Biz? Səhifəsi'

    def __str__(self):
        return self.title


class WhyChooseUsItem(models.Model):
    why_choose_us = models.ForeignKey(WhyChooseUs, on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Başlıq')
    description = models.TextField(blank=True, null=True, verbose_name='Açıqlama')
    icon = models.ImageField(
        upload_to='whyus/', 
        blank=True, 
        null=True, 
        verbose_name='Şəkil',
        help_text='ölçü: 216x214 (enixhundurluyu)'
    )
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Sıra')
    is_active = models.BooleanField(default=True, verbose_name='Aktiv')

    class Meta:
        verbose_name = 'Niyə Biz? Maddəsi'
        verbose_name_plural = 'Niyə Biz? Maddələri'
        ordering = ['order']

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if self.icon:
    #         # Şəkli aç
    #         img = Image.open(self.icon)
            
    #         # Orijinal fayl adı və formatı
    #         original_name = self.icon.name
    #         original_format = img.format or 'PNG'
    #         file_extension = original_name.split('.')[-1].lower()
            
    #         # Menecer tərəfindən təyin edilmiş ölçü
    #         target_width = self.image_width or 216
    #         target_height = self.image_height or 214
            
    #         # Şəkli DƏQİQ ölçüyə gətir (aspect ratio dəyişir)
    #         img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
    #         # Şəkli yaddaşa yaz
    #         output = BytesIO()
            
    #         # PNG formatında saxla (şəffaflıq üçün)
    #         if file_extension == 'png' or img.mode == 'RGBA':
    #             img.save(output, format='PNG', optimize=True)
    #             content_type = 'image/png'
    #             file_ext = 'png'
    #         else:
    #             # JPEG üçün RGB-yə çevir
    #             if img.mode in ('RGBA', 'LA', 'P'):
    #                 background = Image.new('RGB', img.size, (255, 255, 255))
    #                 background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
    #                 img = background
    #             img.save(output, format='JPEG', quality=85, optimize=True)
    #             content_type = 'image/jpeg'
    #             file_ext = 'jpg'
            
    #         output.seek(0)
            
    #         # Yeni faylı yarat
    #         self.icon = InMemoryUploadedFile(
    #             output, 
    #             'ImageField', 
    #             f"{original_name.split('.')[0]}.{file_ext}",
    #             content_type,
    #             sys.getsizeof(output), 
    #             None
    #         )
        
    #     super().save(*args, **kwargs)

class KidContent(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Başlıq', default='Alisa Club Uşaq Kontenti')
    description = models.TextField(
        blank=True, null=True,
        verbose_name='Açıqlama',
        default='Uşaqlar üçün yeni oyunlar, tapşırıqlar və yaradıcı fəaliyyətlər hər həftə'
    )
    center_image = models.ImageField(
        upload_to='kid_content/',
        blank=True, null=True,
        verbose_name='Mərkəz şəkli',
        help_text='Mərkəzdə görünəcək əsas şəkil'
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktiv')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Uşaq Kontenti Səhifəsi'
        verbose_name_plural = 'Uşaq Kontenti Səhifəsi'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Ensure only one active instance exists
        if self.is_active:
            KidContent.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class KidContentItem(models.Model):
    POSITION_CHOICES = [
        ('left', 'Sol sütun'),
        ('right', 'Sağ sütun'),
    ]
    
    kid_content = models.ForeignKey(
        KidContent,
        on_delete=models.CASCADE,
        related_name='items',
        blank=True, null=True,
        verbose_name='Uşaq Kontenti'
    )
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Başlıq')
    description = models.TextField(verbose_name='Qısa mətn', blank=True, null=True)
    image = models.ImageField(upload_to='kid_content/items/', blank=True, null=True, verbose_name='Şəkil')
    position = models.CharField(
        max_length=10,
        choices=POSITION_CHOICES,
        blank=True, null=True,
        verbose_name='Yerləşmə yeri'
    )
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Sıra')
    is_active = models.BooleanField(default=True, verbose_name='Aktiv')
    features = models.TextField(
        verbose_name='Xüsusiyyətlər',
        help_text='Hər xüsusiyyəti yeni sətirdə yazın',
        blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Uşaq Kontenti Maddəsi'
        verbose_name_plural = 'Uşaq Kontenti Maddələri'
        ordering = ['position', 'order']

    def __str__(self):
        return f"{self.get_position_display()} - {self.title}"
    
    def get_features_list(self):
        """Convert the features text field to a list of features."""
        if not self.features:
            return []
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class FAQ(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Başlıq', default='Valideyn Rəyləri')
    subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Alt başlıq', default='Nə deyirlər')
    is_active = models.BooleanField(default=True, verbose_name='Aktiv')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tez-tez verilən suallar' 
        verbose_name_plural = 'Tez-tez verilən suallar'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Ensure only one active instance exists
        if self.is_active:
            FAQ.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class FAQItem(models.Model):
    RATING_CHOICES = [
        (1, '1 Ulduz'),
        (2, '2 Ulduz'),
        (3, '3 Ulduz'),
        (4, '4 Ulduz'),
        (5, '5 Ulduz'),
    ]
    
    faq = models.ForeignKey(
        FAQ,
        on_delete=models.CASCADE,
        related_name='items',
        blank=True, null=True,
        verbose_name='FAQ'
    )
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ad Soyad')
    comment = models.TextField(blank=True, null=True, verbose_name='Rəy')
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=5,
        blank=True, null=True,
        verbose_name='Reytinq'
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktiv')
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Sıra')

    class Meta:
        verbose_name = 'Rəy'
        verbose_name_plural = 'Rəylər'
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.get_rating_display()}"
    
    def get_stars(self):
        """Return the number of filled and empty stars."""
        return {
            'filled': range(self.rating),
            'empty': range(5 - self.rating)
        }


class BirthdayEvent(models.Model):
    title = models.CharField("Başlıq", max_length=200, blank=True, null=True)
    subtitle = models.CharField("Alt başlıq", max_length=200, blank=True, null=True)
    description = models.TextField("Təsvir", blank=True, null=True)
    image = models.ImageField("Şəkil", upload_to='birthday/', blank=True, null=True, help_text='Tövsiyə olunan ölçü: 543x671 piksel')
    button_text = models.CharField("Düymə mətni", max_length=50, default="Ətraflı Bax", blank=True, null=True)

    # Xüsusiyyətlər (dinamik olaraq əlavə etmək üçün)
    class Meta:
        verbose_name = "Doğum Günü Şənliyi"
        verbose_name_plural = "Doğum Günü Şənlikləri"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('birthday')

class BirthdayFeature(models.Model):
    ICON_CHOICES = [
        ('🎈', '🎈 Şar'),
        ('🎉', '🎉 Konfeti'),
        ('🎂', '🎂 Tort'),
        ('🍰', '🍰 Keks'),
        ('🎁', '🎁 Hədiyyə'),
        ('🎮', '🎮 Oyun'),
        ('🎪', '🎪 Sirk'),
        ('🎨', '🎨 Rəsm'),
        ('🎭', '🎭 Maska'),
        ('📸', '📸 Foto'),
        ('🎵', '🎵 Musiqi'),
        ('🎊', '🎊 Bəzək'),
        ('🎀', '🎀 Lent'),
        ('🧁', '🧁 Muffin'),
        ('🍭', '🍭 Şirniyyat'),
    ]
    
    event = models.ForeignKey(BirthdayEvent, on_delete=models.CASCADE, related_name='features', blank=True, null=True, verbose_name="Doğum Günü Şənliyi")
    icon = models.CharField(
        "İkon", 
        max_length=10, 
        choices=ICON_CHOICES,
        default="🎈",
        blank=True, 
        null=True,
        help_text="Siyahıdan emoji seçin"
    )
    text = models.CharField("Xüsusiyyət mətni", max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField("Sıra", default=0, blank=True, null=True)

    class Meta:
        verbose_name = "Xüsusiyyət"
        verbose_name_plural = "Xüsusiyyətlər"
        ordering = ['order']

    def __str__(self):
        return f"{self.icon} {self.text}" if self.icon else self.text


class BirthdayReservationSettings(models.Model):
    """Birthday Reservation Section Settings - Ana səhifə və Birthday səhifəsi üçün"""
    section_title = models.CharField(
        max_length=200, 
        default="Doğum Günü Rezervasiyası", 
        blank=True, 
        null=True, 
        verbose_name="Bölmə Başlığı"
    )
    
    # Feature Items
    feature_1 = models.CharField(
        max_length=200, 
        default="Unudulmaz doğum günü təşkil edin", 
        blank=True, 
        null=True, 
        verbose_name="Xüsusiyyət 1"
    )
    feature_2 = models.CharField(
        max_length=200, 
        default="Rahat və əyləncəli mühit", 
        blank=True, 
        null=True, 
        verbose_name="Xüsusiyyət 2"
    )
    feature_3 = models.CharField(
        max_length=200, 
        default="Foto və video çəkiliş imkanı", 
        blank=True, 
        null=True, 
        verbose_name="Xüsusiyyət 3"
    )
    feature_4 = models.CharField(
        max_length=200, 
        default="Fərdi bəzək və proqram seçimi", 
        blank=True, 
        null=True, 
        verbose_name="Xüsusiyyət 4"
    )
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Rezervasiya Formu Parametrləri"
        verbose_name_plural = "Rezervasiya Formu Parametrləri"

    def __str__(self):
        return "Rezervasiya Formu Parametrləri"

    def save(self, *args, **kwargs):
        if not self.pk and BirthdayReservationSettings.objects.exists():
            raise ValueError('Yalnız bir Rezervasiya Formu Parametrləri yarada bilərsiniz.')
        return super().save(*args, **kwargs)
