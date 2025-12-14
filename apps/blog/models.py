from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class BlogCategory(models.Model):
    """Blog Category"""
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kateqoriya Adı")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name="Slug")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")

    class Meta:
        verbose_name = "Blog Kateqoriyası"
        verbose_name_plural = "Blog Kateqoriyaları"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Blog(models.Model):
    """Blog Post"""
    MEDIA_TYPE_CHOICES = [
        ('image', 'Şəkil'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('gallery', 'Şəkil Qalereyası'),
        ('none', 'Media Yoxdur'),
    ]

    # Basic information
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Başlıq")
    subtitle = models.CharField(max_length=300, blank=True, null=True, verbose_name="Alt Başlıq")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="Slug")
    short_content = models.TextField(max_length=500, blank=True, null=True, verbose_name="Qısa Məzmun")
    full_content = models.TextField(blank=True, null=True, verbose_name="Tam Məzmun")
    
    # Media
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='image', blank=True, null=True, verbose_name="Media Tipi")
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="Şəkil", help_text='Tövsiyə olunan ölçü: 1300x703 piksel')
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL (YouTube/Vimeo)")
    audio_url = models.URLField(blank=True, null=True, verbose_name="Audio URL (SoundCloud)")
    
    # Category and date
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='blogs', verbose_name="Kateqoriya")
    date = models.DateField(blank=True, null=True, verbose_name="Tarix")
    
    # Author information
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name="Müəllif")
    author_image = models.ImageField(upload_to='blog/author/', blank=True, null=True, verbose_name="Müəllif Şəkli", help_text='Tövsiyə olunan ölçü: 180x180 piksel')
    author_bio = models.TextField(blank=True, null=True, verbose_name="Müəllif Haqqında")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True, null=True, verbose_name="Meta Description")
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name="Meta Keywords")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    is_featured = models.BooleanField(default=False, verbose_name="Çox Oxunan")
    show_on_homepage = models.BooleanField(default=False, verbose_name="Ana Səhifədə Göstər")
    homepage_order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Ana Səhifə Sırası")
    show_in_sidebar = models.BooleanField(default=False, verbose_name="Sidebar-da Göstər")
    sidebar_order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sidebar Sırası")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Bloglar"
        ordering = ['-date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def get_previous_blog(self):
        """Previous blog"""
        return Blog.objects.filter(is_active=True, date__lt=self.date).first()

    def get_next_blog(self):
        """Next blog"""
        return Blog.objects.filter(is_active=True, date__gt=self.date).order_by('date').first()


class BlogGallery(models.Model):
    """Blog Image Gallery"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='gallery', blank=True, null=True, verbose_name="Blog")
    image = models.ImageField(upload_to='blog/gallery/', blank=True, null=True, verbose_name="Şəkil", help_text='Tövsiyə olunan ölçü: 100x100 piksel')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Başlıq")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")

    class Meta:
        verbose_name = "Blog Qalereyası"
        verbose_name_plural = "Blog Qalereyaları"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.blog.title} - Şəkil {self.id}"


class SidebarGallery(models.Model):
    """Sidebar Gallery Images"""
    image = models.ImageField(upload_to='sidebar/gallery/', blank=True, null=True, verbose_name="Şəkil", help_text='Tövsiyə olunan ölçü: 100x100 piksel')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Başlıq")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")

    class Meta:
        verbose_name = "Sidebar Qalereyası"
        verbose_name_plural = "Sidebar Qalereyaları"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or f"Şəkil {self.id}"


class BlogPageSettings(models.Model):
    """Blog Page Settings - Breadcrumb and Sidebar Widget"""
    # Breadcrumb settings
    breadcrumb_title = models.CharField(max_length=200, default="Bloqlarımız", blank=True, null=True, verbose_name="Breadcrumb Başlıq")
    breadcrumb_description = models.TextField(max_length=500, default='"Alisa Club" uşaqların inkişafı və öyrənməsi üçün sevgi dolu və hərtərəfli yanaşma təqdim edir', blank=True, null=True, verbose_name="Breadcrumb Təsvir")
    breadcrumb_image = models.ImageField(upload_to='blog/breadcrumb/', blank=True, null=True, verbose_name="Breadcrumb Arxa Fon Şəkli", help_text='Tövsiyə olunan ölçü: 1920x520 piksel')
    
    # Sidebar widget settings
    widget_title = models.CharField(max_length=200, default="Gəlin bir yerdə möhtəşəm işlər yaradaq", blank=True, null=True, verbose_name="Widget Başlıq")
    widget_description = models.TextField(max_length=500, default="Uşaq bağçası ilə bağlı ən son xəbərlər, dəstək və məsləhətlərdən xəbərdar olun.", blank=True, null=True, verbose_name="Widget Təsvir")
    widget_button_text = models.CharField(max_length=50, default="Üzv Ol", blank=True, null=True, verbose_name="Widget Düymə Mətni")
    widget_button_url = models.CharField(max_length=200, default="/registration/", blank=True, null=True, verbose_name="Widget Düymə URL")
    widget_background_image = models.ImageField(upload_to='blog/widget/', blank=True, null=True, verbose_name="Widget Arxa Fon Şəkli")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Blog Səhifə Parametrləri"
        verbose_name_plural = "Blog Səhifə Parametrləri"

    def __str__(self):
        return "Blog Səhifə Parametrləri"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and BlogPageSettings.objects.exists():
            raise ValueError('Yalnız bir Blog Səhifə Parametrləri yarada bilərsiniz. Mövcud olanı redaktə edin.')
        return super().save(*args, **kwargs)


class HomePageBlogSettings(models.Model):
    """Home Page Blog Section Settings"""
    title = models.CharField(max_length=200, default="Son Xəbərlər", blank=True, null=True, verbose_name="Bölmə Başlığı")
    description = models.TextField(max_length=500, default='"Alisa Club"da təqdim olunan fəaliyyətləri və yenilikləri daim genişləndiririk', blank=True, null=True, verbose_name="Bölmə Təsviri")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Ana Səhifə Blog Parametrləri"
        verbose_name_plural = "Ana Səhifə Blog Parametrləri"

    def __str__(self):
        return "Ana Səhifə Blog Parametrləri"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and HomePageBlogSettings.objects.exists():
            raise ValueError('Yalnız bir Ana Səhifə Blog Parametrləri yarada bilərsiniz. Mövcud olanı redaktə edin.')
        return super().save(*args, **kwargs)


class Event(models.Model):
    """Event Model"""
    # Basic information
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tədbir Adı")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="Slug")
    short_description = models.TextField(max_length=500, blank=True, null=True, verbose_name="Qısa Təsvir")
    full_description = models.TextField(blank=True, null=True, verbose_name="Tam Təsvir")
    
    # Event details
    event_date = models.DateTimeField(blank=True, null=True, verbose_name="Başlama Tarixi")
    event_end_date = models.DateTimeField(blank=True, null=True, verbose_name="Bitmə Tarixi", help_text="Bir günlük tədbir üçün boş buraxın")
    location = models.CharField(max_length=300, blank=True, null=True, verbose_name="Yer")
    map_url = models.URLField(blank=True, null=True, verbose_name="Xəritə URL (Google Maps)")
    
    # Coordinator information
    coordinator_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Koordinator Adı")
    coordinator_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Koordinator Telefon")
    coordinator_email = models.EmailField(blank=True, null=True, verbose_name="Koordinator Email")
    
    # Media
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="Tədbir Şəkli", help_text='Tövsiyə olunan ölçü: 1290x640 piksel')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    show_on_homepage = models.BooleanField(default=False, verbose_name="Ana Səhifədə Göstər")
    show_on_hero = models.BooleanField(default=False, verbose_name="Hero Slider-də Göstər")
    show_in_footer = models.BooleanField(default=False, verbose_name="Footer-də Göstər")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    class Meta:
        verbose_name = "Tədbir"
        verbose_name_plural = "Tədbirlər"
        ordering = ['event_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # If this event is set to show in footer, unset all others
        if self.show_in_footer:
            Event.objects.filter(show_in_footer=True).exclude(pk=self.pk).update(show_in_footer=False)
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})

    @property
    def is_upcoming(self):
        """Check if event is upcoming"""
        from django.utils import timezone
        return self.event_date > timezone.now()
    
    def get_duration_days(self):
        """Tədbirin neçə gün davam etdiyini hesabla"""
        if self.event_end_date and self.event_date:
            return (self.event_end_date.date() - self.event_date.date()).days + 1
        return 1


class EventGuide(models.Model):
    """Event Guide - FAQ for events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guides', blank=True, null=True, verbose_name="Tədbir")
    question = models.CharField(max_length=300, blank=True, null=True, verbose_name="Sual")
    answer = models.TextField(blank=True, null=True, verbose_name="Cavab")
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Sıra")

    class Meta:
        verbose_name = "Tədbir Bələdçisi"
        verbose_name_plural = "Tədbir Bələdçiləri"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.event.title} - {self.question}"
