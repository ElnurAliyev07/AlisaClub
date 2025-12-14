from django.contrib import admin
from .models import BlogCategory, Blog, BlogGallery, SidebarGallery, BlogPageSettings, Event, EventGuide, HomePageBlogSettings


class BlogGalleryInline(admin.TabularInline):
    """Blog Gallery Inline"""
    model = BlogGallery
    extra = 1
    fields = ('image', 'title', 'order')
    verbose_name = "Qalereyası Şəkil"
    verbose_name_plural = "Qalereyası Şəkillər"


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    """Blog Category Admin"""
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name', 'slug')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Blog Admin"""
    list_display = ('title', 'category', 'date', 'media_type', 'show_on_homepage', 'show_in_sidebar', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_featured', 'show_on_homepage', 'show_in_sidebar', 'media_type', 'category', 'date')
    search_fields = ('title', 'subtitle', 'short_content', 'full_content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'is_featured', 'show_on_homepage', 'show_in_sidebar')
    date_hierarchy = 'date'
    inlines = [BlogGalleryInline]
    
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('title', 'subtitle', 'slug', 'category', 'date'),
            'description': 'Blog yazısının əsas məlumatlarını daxil edin'
        }),
        ('Məzmun', {
            'fields': ('short_content', 'full_content'),
            'description': 'Qısa məzmun blog siyahısında, tam məzmun isə blog detailində göstəriləcək'
        }),
        ('Media Məlumatları', {
            'fields': ('media_type', 'image', 'video_url', 'audio_url'),
            'description': 'Media tipini seçin və uyğun sahəni doldurun. Qalereyası üçün aşağıdakı bölmədən şəkillər əlavə edin.'
        }),
        ('Müəllif Məlumatları', {
            'fields': ('author', 'author_image', 'author_bio'),
            'classes': ('collapse',),
            'description': 'Müəllif məlumatları (istəyə bağlı)'
        }),
        ('SEO Parametrləri', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',),
            'description': 'Axtarış motorları üçün optimallaşdırma'
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'show_on_homepage', 'homepage_order', 'show_in_sidebar', 'sidebar_order'),
            'description': 'Aktiv: Saytda göstərilsin, Çox Oxunan: Populyar bloglar bölməsində göstərilsin, Ana Səhifədə Göstər: Ana səhifə blog bölməsində göstərilsin (maksimum 3), Sidebar-da Göstər: Base və pagebase sidebar-da "Son Yeniliklər" bölməsində göstərilsin (maksimum 3)'
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category')


@admin.register(BlogGallery)
class BlogGalleryAdmin(admin.ModelAdmin):
    """Blog Gallery Admin"""
    list_display = ('blog', 'title', 'order', 'image')
    list_filter = ('blog',)
    search_fields = ('blog__title', 'title')
    list_editable = ('order',)
    
    fieldsets = (
        ('Qalereyası Məlumatları', {
            'fields': ('blog', 'image', 'title', 'order'),
            'description': 'Şəkil qalereyası üçün şəkil əlavə edin'
        }),
    )


@admin.register(SidebarGallery)
class SidebarGalleryAdmin(admin.ModelAdmin):
    """Sidebar Gallery Admin"""
    list_display = ('title', 'order', 'is_active', 'image', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        ('Şəkil Məlumatları', {
            'fields': ('image', 'title', 'order'),
            'description': 'Sidebar qalereyası üçün şəkil əlavə edin'
        }),
        ('Status', {
            'fields': ('is_active',),
            'description': 'Aktiv şəkillər sidebar-da göstəriləcək'
        }),
    )


@admin.register(BlogPageSettings)
class BlogPageSettingsAdmin(admin.ModelAdmin):
    """Blog Page Settings Admin"""
    
    fieldsets = (
        ('Breadcrumb Parametrləri', {
            'fields': ('breadcrumb_title', 'breadcrumb_description', 'breadcrumb_image'),
            'description': 'Blog səhifəsinin yuxarı hissəsindəki breadcrumb məlumatları'
        }),
        ('Sidebar Widget Parametrləri', {
            'fields': ('widget_title', 'widget_description', 'widget_button_text', 'widget_button_url', 'widget_background_image'),
            'description': 'Sidebar-dakı "Üzv Ol" widget məlumatları'
        }),
        ('Status', {
            'fields': ('is_active',),
            'description': 'Parametrləri aktiv/deaktiv edin'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not BlogPageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(HomePageBlogSettings)
class HomePageBlogSettingsAdmin(admin.ModelAdmin):
    """Home Page Blog Settings Admin"""
    
    fieldsets = (
        ('Ana Səhifə Blog Bölməsi', {
            'fields': ('title', 'description'),
            'description': 'Ana səhifədəki "Son Xəbərlər" bölməsinin başlıq və təsviri'
        }),
        ('Status', {
            'fields': ('is_active',),
            'description': 'Parametrləri aktiv/deaktiv edin'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not HomePageBlogSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


class EventGuideInline(admin.TabularInline):
    """Event Guide Inline"""
    model = EventGuide
    extra = 1
    fields = ('question', 'answer', 'order')
    verbose_name = "Bələdçi Sualı"
    verbose_name_plural = "Bələdçi Sualları"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Event Admin"""
    list_display = ('title', 'event_date', 'event_end_date', 'get_duration', 'location', 'show_on_homepage', 'show_on_hero', 'show_in_footer', 'is_active')
    list_filter = ('is_active', 'show_on_homepage', 'show_on_hero', 'show_in_footer', 'event_date')
    search_fields = ('title', 'short_description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'show_on_homepage', 'show_on_hero', 'show_in_footer')
    date_hierarchy = 'event_date'
    inlines = [EventGuideInline]
    
    def get_duration(self, obj):
        days = obj.get_duration_days()
        return f"{days} gün" if days > 1 else "1 gün"
    get_duration.short_description = 'Müddət'
    
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('title', 'slug'),
            'description': 'Tədbirin adı və URL slug-ı'
        }),
        ('Tarixlər', {
            'fields': ('event_date', 'event_end_date'),
            'description': 'Başlama və bitmə tarixi. Bir günlük tədbir üçün bitmə tarixini boş buraxın.'
        }),
        ('Yer', {
            'fields': ('location', 'map_url'),
            'description': 'Tədbirin keçiriləcəyi yer və Google Maps linki'
        }),
        ('Təsvir', {
            'fields': ('short_description', 'full_description'),
            'description': 'Qısa təsvir: Hero və siyahılarda göstərilir. Tam təsvir: Detail səhifəsində göstərilir.'
        }),
        ('Koordinator Məlumatları', {
            'fields': ('coordinator_name', 'coordinator_phone', 'coordinator_email'),
            'classes': ('collapse',),
            'description': 'Tədbir koordinatorunun əlaqə məlumatları (istəyə görə)'
        }),
        ('Şəkil', {
            'fields': ('image',),
            'description': 'Tədbir şəkli (Hero slaydda və detail səhifəsində göstərilir). Tövsiyə olunan ölçü: 1290x640 piksel'
        }),
        ('Göstərmə Parametrləri', {
            'fields': ('is_active', 'show_on_homepage', 'show_on_hero', 'show_in_footer'),
            'description': '✅ Aktiv: Saytda göstərilsin | ✅ Ana Səhifədə Göstər: Ana səhifə tədbirlər bölməsində göstərilsin | ✅ Hero Slider-də Göstər: Ana səhifə hero slider-də göstərilsin | ✅ Footer-də Göstər: Footer-də geri sayım ilə göstərilsin (yalnız 1 tədbir seçilə bilər)'
        }),
    )


@admin.register(EventGuide)
class EventGuideAdmin(admin.ModelAdmin):
    """Event Guide Admin"""
    list_display = ('event', 'question', 'order')
    list_filter = ('event',)
    search_fields = ('event__title', 'question', 'answer')
    list_editable = ('order',)
    
    fieldsets = (
        ('Bələdçi Məlumatları', {
            'fields': ('event', 'question', 'answer', 'order'),
            'description': 'Tədbir üçün tez-tez verilən suallar'
        }),
    )
