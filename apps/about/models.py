from django.db import models


class AboutPageSettings(models.Model):
    """About Page Settings"""
    # Breadcrumb
    breadcrumb_title = models.CharField(max_length=200, default="Haqqımızda", blank=True, null=True, verbose_name="Breadcrumb Başlıq")
    breadcrumb_description = models.TextField(max_length=500, default="Alisa Club uşaqların inkişafı, yaradıcılığı və öyrənməsini dəstəkləyən sevgi dolu bir mühit yaradır.", blank=True, null=True, verbose_name="Breadcrumb Təsvir")
    breadcrumb_image = models.ImageField(upload_to='about/breadcrumb/', blank=True, null=True, verbose_name="Breadcrumb Arxa Fon", help_text='Tövsiyə olunan ölçü: 1920x520 piksel')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Haqqımızda Səhifə Parametrləri"
        verbose_name_plural = "Haqqımızda Səhifə Parametrləri"

    def __str__(self):
        return "Haqqımızda Səhifə Parametrləri"

    def save(self, *args, **kwargs):
        if not self.pk and AboutPageSettings.objects.exists():
            raise ValueError('Yalnız bir Haqqımızda Səhifə Parametrləri yarada bilərsiniz.')
        return super().save(*args, **kwargs)


class AboutSection(models.Model):
    """About Section - Two sections with image and text"""
    POSITION_CHOICES = [
        ('left', 'Sol'),
        ('right', 'Sağ'),
    ]
    
    title = models.CharField(max_length=300, blank=True, null=True, verbose_name="Başlıq")
    description = models.TextField(blank=True, null=True, verbose_name="Təsvir")
    image = models.ImageField(upload_to='about/sections/', blank=True, null=True, verbose_name="Şəkil", help_text='Tövsiyə olunan ölçü: 618x618 piksel')
    image_position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='right', blank=True, null=True, verbose_name="Şəkil Mövqeyi")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")

    class Meta:
        verbose_name = "Haqqımızda Bölməsi"
        verbose_name_plural = "Haqqımızda Bölmələri"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class AboutSectionFeature(models.Model):
    """Features for About Section"""
    section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='features', blank=True, null=True, verbose_name="Bölmə")
    text = models.CharField(max_length=200, blank=True, null=True, verbose_name="Xüsusiyyət Mətni")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")

    class Meta:
        verbose_name = "Bölmə Xüsusiyyəti"
        verbose_name_plural = "Bölmə Xüsusiyyətləri"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.section.title} - {self.text}"


class SessionTime(models.Model):
    """Session Times"""
    section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='session_times', blank=True, null=True, verbose_name="Bölmə")
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Seans Adı")
    time = models.CharField(max_length=50, blank=True, null=True, verbose_name="Vaxt")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")

    class Meta:
        verbose_name = "Seans Vaxtı"
        verbose_name_plural = "Seans Vaxtları"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.title}: {self.time}"


class Timeline(models.Model):
    """Timeline/History"""
    year = models.CharField(max_length=4, blank=True, null=True, verbose_name="İl")
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Başlıq")
    description = models.TextField(blank=True, null=True, verbose_name="Təsvir")
    image = models.ImageField(upload_to='about/timeline/', blank=True, null=True, verbose_name="Şəkil", help_text='Tövsiyə olunan ölçü: 300x150 piksel')
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")

    class Meta:
        verbose_name = "Tarixçə"
        verbose_name_plural = "Tarixçələr"
        ordering = ['order', 'year']

    def __str__(self):
        return f"{self.year} - {self.title}"


class TimelineSettings(models.Model):
    """Timeline Section Settings"""
    subtitle = models.CharField(max_length=200, default="Alisa Club tarixçəsi", blank=True, null=True, verbose_name="Alt Başlıq")
    title = models.CharField(max_length=300, default="İllərlə böyüyən sevgi və inkişafa səyahət", blank=True, null=True, verbose_name="Başlıq")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Tarixçə Bölməsi Parametrləri"
        verbose_name_plural = "Tarixçə Bölməsi Parametrləri"

    def __str__(self):
        return "Tarixçə Bölməsi Parametrləri"

    def save(self, *args, **kwargs):
        if not self.pk and TimelineSettings.objects.exists():
            raise ValueError('Yalnız bir Tarixçə Bölməsi Parametrləri yarada bilərsiniz.')
        return super().save(*args, **kwargs)


class Gallery(models.Model):
    """Gallery Images"""
    image = models.ImageField(upload_to='about/gallery/', blank=True, null=True, verbose_name="Şəkil", help_text='Tövsiyə olunan ölçü: 290x253 piksel')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Başlıq")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")

    class Meta:
        verbose_name = "Qalereyası"
        verbose_name_plural = "Qalereyaları"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or f"Şəkil {self.id}"


class GallerySettings(models.Model):
    """Gallery Section Settings"""
    title = models.CharField(max_length=300, default="Alisa Club-un rəngarəng dünyasına baxın!", blank=True, null=True, verbose_name="Başlıq")
    description = models.TextField(max_length=500, default="Kiçik ürəklərin böyük gülümsəmələri — hər anı sevgi ilə paylaşırıq", blank=True, null=True, verbose_name="Təsvir")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Qalereyası Bölməsi Parametrləri"
        verbose_name_plural = "Qalereyası Bölməsi Parametrləri"

    def __str__(self):
        return "Qalereyası Bölməsi Parametrləri"

    def save(self, *args, **kwargs):
        if not self.pk and GallerySettings.objects.exists():
            raise ValueError('Yalnız bir Qalereyası Bölməsi Parametrləri yarada bilərsiniz.')
        return super().save(*args, **kwargs)
