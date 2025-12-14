from django.contrib import admin
from .models import ServicePageSettings, Service, ServiceFeature, ServiceSchedule, ServiceFAQ


@admin.register(ServicePageSettings)
class ServicePageSettingsAdmin(admin.ModelAdmin):
    """Service Page Settings Admin"""
    
    fieldsets = (
        ('Breadcrumb Parametrləri', {
            'fields': ('breadcrumb_title', 'breadcrumb_description', 'breadcrumb_image'),
        }),
        ('Üst Bölmə', {
            'fields': ('top_section_title', 'top_section_description'),
        }),
        ('Orta Bölmə', {
            'fields': ('middle_section_subtitle', 'middle_section_title'),
        }),
        ('CTA Bölməsi', {
            'fields': ('cta_title', 'cta_description', 'cta_button_text'),
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )
    
    def has_add_permission(self, request):
        return not ServicePageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ('feature_text', 'order')


class ServiceScheduleInline(admin.TabularInline):
    model = ServiceSchedule
    extra = 1
    fields = ('session_name', 'time_range', 'order')


class ServiceFAQInline(admin.StackedInline):
    model = ServiceFAQ
    extra = 1
    fields = ('question', 'answer', 'order', 'is_active')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Service Admin"""
    list_display = ('title', 'show_in_featured', 'show_in_standard', 'show_in_values', 'order', 'is_active', 'created_at')
    list_filter = ('show_in_featured', 'show_in_standard', 'show_in_values', 'is_active', 'created_at')
    search_fields = ('title', 'short_description', 'description')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceFeatureInline, ServiceScheduleInline, ServiceFAQInline]
    
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('title', 'slug', 'short_description', 'description'),
        }),
        ('Şəkillər', {
            'fields': ('icon_path', 'image', 'detail_image'),
            'description': 'İkon yolu statik faylların yolunu göstərir (məsələn: assets/img/icon/sr-1-1.svg)'
        }),
        ('Göstərilmə Yerləri', {
            'fields': ('show_in_featured', 'show_in_standard', 'show_in_values'),
            'description': 'Xidmətin hansı bölmələrdə göstəriləcəyini seçin'
        }),
        ('Parametrlər', {
            'fields': ('order', 'is_active'),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('features', 'schedules', 'faqs')


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    """Service Feature Admin"""
    list_display = ('service', 'feature_text', 'order')
    list_filter = ('service',)
    search_fields = ('feature_text',)
    list_editable = ('order',)


@admin.register(ServiceSchedule)
class ServiceScheduleAdmin(admin.ModelAdmin):
    """Service Schedule Admin"""
    list_display = ('service', 'session_name', 'time_range', 'order')
    list_filter = ('service',)
    search_fields = ('session_name',)
    list_editable = ('order',)


@admin.register(ServiceFAQ)
class ServiceFAQAdmin(admin.ModelAdmin):
    """Service FAQ Admin"""
    list_display = ('service', 'question', 'order', 'is_active')
    list_filter = ('service', 'is_active')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')
