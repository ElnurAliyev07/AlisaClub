from django.contrib import admin
from .models import (
    AboutPageSettings, AboutSection, AboutSectionFeature, SessionTime,
    Timeline, TimelineSettings, Gallery, GallerySettings
)


class AboutSectionFeatureInline(admin.TabularInline):
    """About Section Features Inline"""
    model = AboutSectionFeature
    extra = 1
    fields = ('text', 'order')
    verbose_name = "Xüsusiyyət"
    verbose_name_plural = "Xüsusiyyətlər"


class SessionTimeInline(admin.TabularInline):
    """Session Times Inline"""
    model = SessionTime
    extra = 1
    fields = ('title', 'time', 'order')
    verbose_name = "Seans Vaxtı"
    verbose_name_plural = "Seans Vaxtları"


@admin.register(AboutPageSettings)
class AboutPageSettingsAdmin(admin.ModelAdmin):
    """About Page Settings Admin"""
    
    fieldsets = (
        ('Breadcrumb Parametrləri', {
            'fields': ('breadcrumb_title', 'breadcrumb_description', 'breadcrumb_image'),
            'description': 'Haqqımızda səhifəsinin yuxarı hissəsindəki breadcrumb məlumatları'
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )
    
    def has_add_permission(self, request):
        return not AboutPageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    """About Section Admin"""
    list_display = ('title', 'image_position', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'image_position')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    inlines = [AboutSectionFeatureInline, SessionTimeInline]
    
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('title', 'description', 'image', 'image_position', 'order'),
            'description': 'Haqqımızda bölməsinin məlumatları. Şəkil mövqeyi: Sol və ya Sağ'
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )


@admin.register(TimelineSettings)
class TimelineSettingsAdmin(admin.ModelAdmin):
    """Timeline Settings Admin"""
    
    fieldsets = (
        ('Tarixçə Bölməsi', {
            'fields': ('subtitle', 'title'),
            'description': 'Tarixçə bölməsinin başlıq və alt başlığı'
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )
    
    def has_add_permission(self, request):
        return not TimelineSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    """Timeline Admin"""
    list_display = ('year', 'title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'year')
    search_fields = ('year', 'title', 'description')
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        ('Tarixçə Məlumatları', {
            'fields': ('year', 'title', 'description', 'image', 'order'),
            'description': 'Tarixçə üçün il, başlıq, təsvir və şəkil əlavə edin'
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )


@admin.register(GallerySettings)
class GallerySettingsAdmin(admin.ModelAdmin):
    """Gallery Settings Admin"""
    
    fieldsets = (
        ('Qalereyası Bölməsi', {
            'fields': ('title', 'description'),
            'description': 'Qalereyası bölməsinin başlıq və təsviri'
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )
    
    def has_add_permission(self, request):
        return not GallerySettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Gallery Admin"""
    list_display = ('title', 'order', 'is_active', 'image', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        ('Qalereyası Məlumatları', {
            'fields': ('image', 'title', 'order'),
            'description': 'Qalereyası üçün şəkil əlavə edin'
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )
