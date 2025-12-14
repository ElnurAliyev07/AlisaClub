from django.contrib import admin
from django.utils.html import format_html
from .models_profile import ParentProfile, Child, MedalType, Medal, Discount

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'get_status', 'get_medal_count', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    
    def get_status(self, obj):
        return obj.get_status()
    get_status.short_description = 'Status'


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'birth_date', 'get_age', 'is_birthday_soon', 'photo_preview']
    search_fields = ['name', 'parent__user__first_name', 'parent__user__last_name']
    list_filter = ['birth_date']
    date_hierarchy = 'birth_date'
    readonly_fields = ['photo_preview']
    
    fieldsets = (
        ('Uşaq Məlumatları', {
            'fields': ('parent', 'name', 'birth_date')
        }),
        ('Şəkil', {
            'fields': ('photo', 'photo_preview'),
            'description': 'Uşağın profil şəkli (medallar üçün istifadə olunur)'
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%;" />', obj.photo.url)
        return "-"
    photo_preview.short_description = 'Şəkil Önizləməsi'
    
    def get_age(self, obj):
        return f"{obj.get_age()} yaş"
    get_age.short_description = 'Yaş'
    
    def is_birthday_soon(self, obj):
        return "✅ Bəli" if obj.is_birthday_soon() else "❌ Xeyr"
    is_birthday_soon.short_description = 'Doğum günü yaxınlaşır?'


@admin.register(MedalType)
class MedalTypeAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'description']
    search_fields = ['name', 'description']


@admin.register(Medal)
class MedalAdmin(admin.ModelAdmin):
    list_display = ['child', 'get_parent_name', 'medal_type', 'event_name', 'show_on_homepage', 'awarded_at']
    search_fields = ['child__name', 'child__parent__user__first_name', 'child__parent__user__last_name', 'event_name']
    list_filter = ['medal_type', 'show_on_homepage', 'awarded_at']
    list_editable = ['show_on_homepage']
    date_hierarchy = 'awarded_at'
    
    fieldsets = (
        ('Medal Məlumatı', {
            'fields': ('child', 'medal_type', 'reason'),
            'description': 'Uşağa verilən medal məlumatları'
        }),
        ('Tədbir Məlumatı (İstəyə görə)', {
            'fields': ('event_name', 'event_date'),
            'classes': ('collapse',),
            'description': 'Medal tədbir ilə əlaqəlidirsə doldurun'
        }),
        ('Göstərmə Parametrləri', {
            'fields': ('show_on_homepage',),
            'description': 'Ana səhifədə göstərilsin?'
        }),
    )
    
    def get_parent_name(self, obj):
        return obj.child.parent.user.get_full_name()
    get_parent_name.short_description = 'Valideyn'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "child":
            kwargs["queryset"] = Child.objects.select_related('parent__user').order_by('parent__user__first_name', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_percent', 'code', 'valid_from', 'valid_until', 'show_on_homepage', 'is_active', 'is_valid']
    search_fields = ['title', 'code', 'description']
    list_filter = ['is_active', 'show_on_homepage', 'valid_from', 'valid_until']
    list_editable = ['show_on_homepage', 'is_active']
    date_hierarchy = 'valid_from'
    readonly_fields = ['created_at', 'image_preview']
    
    fieldsets = (
        ('Kampaniya Məlumatı', {
            'fields': ('title', 'description', 'discount_percent', 'code'),
            'description': 'Kampaniyanın əsas məlumatları'
        }),
        ('Şəkil', {
            'fields': ('image', 'image_preview'),
            'description': 'Kampaniya şəkli (istəyə görə)'
        }),
        ('Tarixlər', {
            'fields': ('valid_from', 'valid_until'),
            'description': 'Kampaniyanın etibarlılıq müddəti'
        }),
        ('Göstərmə Parametrləri', {
            'fields': ('is_active', 'show_on_homepage'),
            'description': 'Kampaniya aktiv və ana səhifədə göstərilsin?'
        }),
        ('Sistem', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def is_valid(self, obj):
        if obj.is_valid():
            days_left = obj.get_days_left()
            return format_html('<span style="color: green;">✅ Etibarlı ({} gün qalıb)</span>', days_left)
        return format_html('<span style="color: red;">❌ Etibarsız</span>')
    is_valid.short_description = 'Etibarlılıq'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Şəkil Önizləməsi'
