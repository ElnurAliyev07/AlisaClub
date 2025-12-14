from django.db import models
from django.utils.text import slugify


class ServicePageSettings(models.Model):
    # Breadcrumb
    breadcrumb_title = models.CharField(max_length=200, default="Xidmətlər", blank=True, null=True, verbose_name="Breadcrumb Başlıq")
    breadcrumb_description = models.TextField(max_length=500, default="Alisa Club uşaqlar üçün əyləncəli və öyrədici fəaliyyətlər təqdim edir", blank=True, null=True, verbose_name="Breadcrumb Təsvir")
    breadcrumb_image = models.ImageField(upload_to='services/breadcrumb/', blank=True, null=True, verbose_name="Breadcrumb Arxa Fon", help_text='Tövsiyə olunan ölçü: 1920x520 piksel')
    
    # Top Section
    top_section_title = models.CharField(max_length=300, default="Uşağınızı İndi Proqrama Qeydiyyatdan Keçirin!", blank=True, null=True, verbose_name="Üst Bölmə Başlığı")
    top_section_description = models.TextField(default="Alisa Club-da hər uşaq üçün açıq qapı siyasəti mövcuddur və bütün uşaqlar üçün pulsuz sınaq dərsi təklif olunur.", blank=True, null=True, verbose_name="Üst Bölmə Təsviri")
    
    # Middle Section
    middle_section_subtitle = models.CharField(max_length=200, default="Bizim Təklif Etdiyimiz Xidmətlər", blank=True, null=True, verbose_name="Orta Bölmə Alt Başlığı")
    middle_section_title = models.CharField(max_length=300, default="Uşağınızı fəaliyyətlərdə düzgün istiqamətləndirmək və dəstək olmaq üçün buradayıq", blank=True, null=True, verbose_name="Orta Bölmə Başlığı")
    

    
    # CTA Section
    cta_title = models.CharField(max_length=300, default="Gəlin birlikdə möhtəşəm anlar yaradaq", blank=True, null=True, verbose_name="CTA Başlığı")
    cta_description = models.TextField(default="Uşağınızın inkişafı, təlimi və klubdakı fəaliyyətləri barədə ən son məlumatları, dəstək və tövsiyələri əldə edin.", blank=True, null=True, verbose_name="CTA Təsviri")
    cta_button_text = models.CharField(max_length=50, default="Üzv Ol", blank=True, null=True, verbose_name="CTA Düymə Mətni")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Xidmətlər Səhifə Parametrləri"
        verbose_name_plural = "Xidmətlər Səhifə Parametrləri"

    def __str__(self):
        return "Xidmətlər Səhifə Parametrləri"

    def save(self, *args, **kwargs):
        if not self.pk and ServicePageSettings.objects.exists():
            raise ValueError('Yalnız bir Xidmətlər Səhifə Parametrləri yarada bilərsiniz.')
        return super().save(*args, **kwargs)


class Service(models.Model):
    """Service Model"""
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Başlıq")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="Slug")
    short_description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Qısa Təsvir")
    description = models.TextField(blank=True, null=True, verbose_name="Təsvir")
    
    # Images
    icon_path = models.CharField(max_length=200, default='assets/img/icon/sr-1-1.svg', blank=True, null=True, verbose_name="İkon Yolu", 
                                 help_text="Məsələn: assets/img/icon/sr-1-1.svg")
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Şəkil", help_text='Tövsiyə olunan ölçü: 300x380 piksel')
    detail_image = models.ImageField(upload_to='services/detail/', blank=True, null=True, verbose_name="Detail Şəkil", help_text='Tövsiyə olunan ölçü: 640x640 piksel')
    
    # Service Display Options (Checkboxes)
    show_in_featured = models.BooleanField(default=False, verbose_name="Seçilmiş Xidmətlərdə Göstər")
    show_in_standard = models.BooleanField(default=True, verbose_name="Standart Xidmətlərdə Göstər")
    show_in_values = models.BooleanField(default=False, verbose_name="Dəyərlər Bölməsində Göstər")
    
    # Order and Status
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Xidmət"
        verbose_name_plural = "Xidmətlər"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ServiceFeature(models.Model):
    """Service Features"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features', blank=True, null=True, verbose_name="Xidmət")
    feature_text = models.CharField(max_length=300, blank=True, null=True, verbose_name="Xüsusiyyət")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")

    class Meta:
        verbose_name = "Xidmət Xüsusiyyəti"
        verbose_name_plural = "Xidmət Xüsusiyyətləri"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.service.title} - {self.feature_text[:50]}"


class ServiceSchedule(models.Model):
    """Service Schedule"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='schedules', blank=True, null=True, verbose_name="Xidmət")
    session_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sessiya Adı")
    time_range = models.CharField(max_length=100, blank=True, null=True, verbose_name="Vaxt Aralığı")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")

    class Meta:
        verbose_name = "Xidmət Cədvəli"
        verbose_name_plural = "Xidmət Cədvəlləri"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.service.title} - {self.session_name}"


class ServiceFAQ(models.Model):
    """Service FAQ"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='faqs', blank=True, null=True, verbose_name="Xidmət")
    question = models.CharField(max_length=300, blank=True, null=True, verbose_name="Sual")
    answer = models.TextField(blank=True, null=True, verbose_name="Cavab")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")

    class Meta:
        verbose_name = "Xidmət FAQ"
        verbose_name_plural = "Xidmət FAQ-lar"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.service.title} - {self.question[:50]}"
