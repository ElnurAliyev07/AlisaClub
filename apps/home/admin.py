from django.contrib import admin
from django.utils.html import format_html
from django.forms import Textarea
from django.db import models
from .models import (
    Hero, About, SessionTime, WhyChooseUs, WhyChooseUsItem, 
    KidContent, KidContentItem, FAQ, FAQItem, 
    BirthdayEvent, BirthdayFeature, BirthdayReservationSettings
)


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'event_description', 'image')


class SessionTimeInline(admin.TabularInline):
    model = SessionTime
    extra = 1
    fields = ('period', 'time_range')


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'stat_1_value', 'stat_2_value')
    list_display_links = ('title',)
    fieldsets = (
        ('Əsas məlumatlar', {
            'fields': ('subtitle', 'title', 'description')
        }),
        ('Şəkillər', {
            'fields': ('image_1', 'image_2', 'image_3', 'image_4'),
            'description': 'Tövsiyə olunan ölçü: 281x274 piksel'
        }),
        ('Statistika 1', {
            'fields': ('stat_1_value', 'stat_1_text'),
            'description': 'Birinci statistika məlumatı'
        }),
        ('Statistika 2', {
            'fields': ('stat_2_value', 'stat_2_text'),
            'description': 'İkinci statistika məlumatı'
        }),
        ('Dərs cədvəli', {
            'fields': ('session_days',),
            'description': 'Dərs günləri ilə bağlı məlumat'
        }),
    )
    inlines = [SessionTimeInline]


@admin.register(SessionTime)
class SessionTimeAdmin(admin.ModelAdmin):
    list_display = ('get_period_display', 'time_range', 'about')
    list_filter = ('period',)
    search_fields = ('time_range', 'about__title')
    list_select_related = ('about',)


class WhyChooseUsItemInline(admin.TabularInline):
    model = WhyChooseUsItem
    extra = 1
    fields = ('title', 'description',  'icon', 'order', 'is_active')
    readonly_fields = ('preview_icon',)
    
    def preview_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.icon.url)
        return "(No icon)"
    preview_icon.short_description = 'İkon Önizleme'


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('title', 'subtitle', 'description', 'is_active')
        }),
    )
    inlines = [WhyChooseUsItemInline]
    
    def has_add_permission(self, request):
        # Allow only one instance
        if self.model.objects.count() >= 1:
            return False
        return True


@admin.register(WhyChooseUsItem)
class WhyChooseUsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'why_choose_us', 'order', 'is_active')
    list_filter = ('is_active', 'why_choose_us')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    readonly_fields = ('preview_icon',)
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('why_choose_us', 'title', 'description', 'order', 'is_active')
        }),
        ('Şəkil Parametrləri', {
            'fields': ( 'icon', 'preview_icon'),
            'description': 'Əvvəlcə şəkil ölçülərini təyin edin, sonra şəkli yükləyin'
        }),
    )
    
    def preview_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.icon.url)
        return "(No icon)"
    preview_icon.short_description = 'İkon Önizleme'


# class KidContentItemInline(admin.TabularInline):
#     model = KidContentItem
#     extra = 1
#     formfield_overrides = {
#         models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
#     }
#     fields = ('title', 'description', 'image', 'position', 'order', 'features', 'is_active')
#     readonly_fields = ('preview_image',)
    
#     def preview_image(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
#         return "(No image)"
#     preview_image.short_description = 'Şəkil Önizleme'


# @admin.register(KidContent)
# class KidContentAdmin(admin.ModelAdmin):
#     list_display = ('title', 'is_active', 'created_at', 'updated_at')
#     list_editable = ('is_active',)
#     fieldsets = (
#         ('Əsas Məlumatlar', {
#             'fields': ('title', 'description', 'center_image', 'is_active')
#         }),
#     )
#     inlines = [KidContentItemInline]
#     readonly_fields = ('created_at', 'updated_at')
    
#     def has_add_permission(self, request):
#         # Allow only one instance
#         if self.model.objects.count() >= 1:
#             return False
#         return True


# @admin.register(KidContentItem)
# class KidContentItemAdmin(admin.ModelAdmin):
#     list_display = ('title', 'kid_content', 'get_position_display', 'order', 'is_active')
#     list_filter = ('is_active', 'position', 'kid_content')
#     list_editable = ('order', 'is_active')
#     search_fields = ('title', 'description')
#     readonly_fields = ('preview_image',)
#     formfield_overrides = {
#         models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
#     }
    
#     def preview_image(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.image.url)
#         return "(No image)"
#     preview_image.short_description = 'Şəkil Önizleme'


class FAQItemInline(admin.TabularInline):
    model = FAQItem
    extra = 1
    fields = ('name', 'comment', 'rating', 'is_active', 'order')
    readonly_fields = ('preview_rating',)
    
    def preview_rating(self, obj):
        filled_stars = '★' * obj.rating
        empty_stars = '☆' * (5 - obj.rating)
        return format_html('<div style="font-size: 1.2em; color: gold;">{}{}</div>', 
                         filled_stars, empty_stars)
    preview_rating.short_description = 'Reytinq Önizleme'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'is_active', 'created_at')
    list_editable = ('is_active',)
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('title', 'subtitle', 'is_active')
        }),
    )
    inlines = [FAQItemInline]
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Allow only one instance
        if self.model.objects.count() >= 1:
            return False
        return True


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview_rating', 'is_active', 'order')
    list_filter = ('is_active', 'rating')
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'comment')
    readonly_fields = ('preview_rating',)
    
    def preview_rating(self, obj):
        filled_stars = '★' * obj.rating
        empty_stars = '☆' * (5 - obj.rating)
        return format_html('<div style="font-size: 1.5em; color: gold;">{}{}</div>', 
                         filled_stars, empty_stars)
    preview_rating.short_description = 'Reytinq'




class BirthdayFeatureInline(admin.TabularInline):
    model = BirthdayFeature
    extra = 3
    fields = ('icon', 'text', 'order')
    verbose_name = "Xüsusiyyət"
    verbose_name_plural = "Xüsusiyyətlər (İkon və mətn əlavə edin)"

@admin.register(BirthdayEvent)
class BirthdayEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'button_text')
    inlines = [BirthdayFeatureInline]
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('title', 'subtitle', 'description'),
            'description': 'Ana səhifədə göstəriləcək doğum günü şənliyi məlumatları'
        }),
        ('Şəkil və Düymə', {
            'fields': ('image', 'button_text'),
            'description': 'Şəkil və düymə mətni'
        }),
    )

    def has_add_permission(self, request):
        # Yalnız 1 obyekt olsun (singleton)
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(BirthdayFeature)
class BirthdayFeatureAdmin(admin.ModelAdmin):
    list_display = ('get_icon_display', 'text', 'event', 'order')
    list_editable = ('order',)
    list_filter = ('event', 'icon')
    search_fields = ('text',)
    fieldsets = (
        ('Xüsusiyyət Məlumatları', {
            'fields': ('event', 'icon', 'text', 'order'),
            'description': 'Siyahıdan uyğun emoji seçin və xüsusiyyət mətnini yazın'
        }),
    )
    
    def get_icon_display(self, obj):
        return format_html('<span style="font-size: 1.5em;">{}</span>', obj.icon)
    get_icon_display.short_description = 'İkon'



@admin.register(BirthdayReservationSettings)
class BirthdayReservationSettingsAdmin(admin.ModelAdmin):
    """Birthday Reservation Settings Admin"""
    list_display = ('section_title', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Bölmə Başlığı', {
            'fields': ('section_title',),
            'description': 'Ana səhifə və Birthday səhifəsində göstəriləcək rezervasiya formu başlığı'
        }),
        ('Xüsusiyyətlər', {
            'fields': ('feature_1', 'feature_2', 'feature_3', 'feature_4'),
            'description': 'Rezervasiya formu üzərində göstəriləcək xüsusiyyətlər'
        }),
        ('Status', {
            'fields': ('is_active', 'updated_at'),
        }),
    )
    
    def has_add_permission(self, request):
        return not BirthdayReservationSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
