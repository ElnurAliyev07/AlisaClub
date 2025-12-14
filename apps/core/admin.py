from django.contrib import admin
from django.utils.html import format_html
from .models import SocialLink, SiteLogo, ContactInfo, FooterInfo, PageSEO
from .admin_profile import *


# --- SocialLink ---
@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('facebook', 'instagram', 'youtube', 'telegram')

# --- SiteLogo ---
@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'footer_logo_preview', 'header_logo_preview')
    search_fields = ('alt_text',)

    def footer_logo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius:4px; background:#333; padding:5px;" />', obj.image.url)
        return "-"
    footer_logo_preview.short_description = "Footer Logo (Ağ)"

    def header_logo_preview(self, obj):
        if obj.header_logo:
            return format_html('<img src="{}" width="100" style="border-radius:4px; background:#fff; padding:5px;" />', obj.header_logo.url)
        return "-"
    header_logo_preview.short_description = "Header Logo (Qara)"


# --- ContactInfo ---
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address', 'filial_address', 'filial_phone', 'work_days', 'map_embed')
    search_fields = ('phone', 'email', 'address')
    fieldsets = (
        (None, {
            'fields': ('phone', 'email', 'address', 'filial_address', 'filial_phone', 'work_days', 'map_embed')
        }),
    )


# --- FooterInfo ---
@admin.register(FooterInfo)
class FooterInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'copyright_text', 'rights_reserved', 'creation_text', 'creation_url')
    search_fields = (
        'title',
        'copyright_text',
        'rights_reserved',
        'creation_text',
        'creation_url'
    )


@admin.register(PageSEO)
class PageSEOAdmin(admin.ModelAdmin):
    list_display = ['page_type', 'get_seo_title', 'get_og_title', 'no_index', 'no_follow']
    list_editable = ['no_index', 'no_follow']

    fieldsets = (
        ('Səhifə Məlumatları', {
            'fields': ('page_type',),
        }),
        ('Meta Məlumatları', {
            'fields': ('seo_title', 'seo_description', 'meta_keywords', 'canonical_url'),
        }),
        ('Open Graph', {
            'fields': ('og_title', 'og_description', 'og_image'),
        }),
        ('Brendinq', {
            'fields': ('logo',),
        }),
        ('Robotlar', {
            'fields': ('no_index', 'no_follow'),
        }),
    )

    def get_seo_title(self, obj):
        return obj.seo_title
    get_seo_title.short_description = 'SEO Title'

    def get_og_title(self, obj):
        return obj.og_title
    get_og_title.short_description = 'OG Title'
