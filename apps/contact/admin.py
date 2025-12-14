from django.contrib import admin
from .models import Contact, ContactMessage


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'image')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Contact Message Admin"""
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('first_name', 'last_name', 'email', 'phone', 'message', 'created_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Göndərən Məlumatları', {
            'fields': ('first_name', 'last_name', 'email', 'phone'),
        }),
        ('Mesaj', {
            'fields': ('message',),
        }),
        ('Admin Sahələri', {
            'fields': ('is_read', 'notes', 'created_at'),
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} mesaj oxundu olaraq işarələndi.')
    mark_as_read.short_description = 'Seçilmişləri oxundu olaraq işarələ'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} mesaj oxunmamış olaraq işarələndi.')
    mark_as_unread.short_description = 'Seçilmişləri oxunmamış olaraq işarələ'
