from django.contrib import admin
from .models import BirthdayPageSettings, BirthdayGallery, BirthdayReservation


@admin.register(BirthdayPageSettings)
class BirthdayPageSettingsAdmin(admin.ModelAdmin):
    """Birthday Page Settings Admin"""
    
    fieldsets = (
        ('Breadcrumb Parametrləri', {
            'fields': ('breadcrumb_title', 'breadcrumb_description', 'breadcrumb_image'),
            'description': 'Doğum günü səhifəsinin yuxarı hissəsindəki breadcrumb məlumatları'
        }),
        ('Hero Bölməsi', {
            'fields': ('hero_subtitle', 'hero_title', 'hero_description', 'hero_image', 'hero_button_text', 'hero_button_url'),
            'description': 'Səhifənin əsas hero bölməsi məlumatları'
        }),
        ('Qalereyası Bölməsi', {
            'fields': ('gallery_subtitle', 'gallery_title'),
            'description': 'Qalereyası bölməsinin başlıq və alt başlığı'
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )
    
    def has_add_permission(self, request):
        return not BirthdayPageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BirthdayGallery)
class BirthdayGalleryAdmin(admin.ModelAdmin):
    """Birthday Gallery Admin"""
    list_display = ('title', 'order', 'is_active', 'image', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        ('Qalereyası Məlumatları', {
            'fields': ('image', 'title', 'order'),
            'description': 'Doğum günü qalereyası üçün şəkil əlavə edin'
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )


@admin.register(BirthdayReservation)
class BirthdayReservationAdmin(admin.ModelAdmin):
    """Birthday Reservation Admin"""
    list_display = ('child_name', 'event_date', 'parent_name', 'phone', 'participants', 'is_read', 'created_at')
    list_filter = ('is_read', 'subscribe_to_events', 'event_date', 'created_at')
    search_fields = ('child_name', 'parent_name', 'email', 'phone')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Uşaq Məlumatları', {
            'fields': ('child_name', 'birth_date'),
        }),
        ('Şənlik Məlumatları', {
            'fields': ('event_date', 'participants', 'notes'),
            'description': 'Doğum günü şənliyinin keçiriləcəyi tarix və detallar'
        }),
        ('Valideyn Məlumatları', {
            'fields': ('parent_name', 'phone', 'email'),
        }),
        ('Əlavə Məlumatlar', {
            'fields': ('subscribe_to_events',),
        }),
        ('Admin Sahələri', {
            'fields': ('is_read', 'admin_notes', 'created_at'),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} rezervasiya oxundu olaraq işarələndi.')
    mark_as_read.short_description = 'Seçilmişləri oxundu olaraq işarələ'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} rezervasiya oxunmamış olaraq işarələndi.')
    mark_as_unread.short_description = 'Seçilmişləri oxunmamış olaraq işarələ'
