from django.db import models
from django.core.cache import cache
from .models_profile import ParentProfile, Child, MedalType, Medal, Discount

class SocialLink(models.Model):
    facebook=models.URLField(
        verbose_name="Facebook Linki",
        blank=True, null=True
    )
    instagram=models.URLField(
        verbose_name="Instagram Linki",
        blank=True, null=True
    )
    youtube=models.URLField(
        verbose_name="YouTube Linki",
        blank=True, null=True
    )
    telegram=models.URLField(
        verbose_name="Telegram Linki",
        blank=True, null=True
    )


class SiteLogo(models.Model):
    alt_text=models.CharField(
        max_length=100,
        verbose_name='Alt mətn',
        blank=True, null=True
    )
    image = models.ImageField(
        upload_to='logos/',  
        verbose_name='Logo Şəkli (Footer üçün - Ağ rəng)',
        blank=True, null=True
    )
    header_logo = models.ImageField(
        upload_to='logos/',  
        verbose_name='Header Logo (Qara rəng)',
        blank=True, null=True,
        help_text='Header üçün qara rəngdə logo'
    )

    class Meta:
        verbose_name = 'Sayt Logo'
        verbose_name_plural = 'Logo'

    def __str__(self):
        return self.alt_text or f"Logo #{self.pk}"


class ContactInfo(models.Model):
    phone = models.CharField(max_length=50, verbose_name="Telefon Nömrəsi", blank=True, null=True)
    email = models.EmailField(verbose_name="E-poçt", blank=True, null=True)
    address = models.CharField(
        max_length=250,
        verbose_name="Ünvan",
        blank=True, null=True,
        default="Atatür prospekti 1010"
    )
    filial_address=models.CharField(
        max_length=250,
        verbose_name="Filial Ünvanı",
        blank=True, null=True
    )
    filial_phone=models.CharField(
        max_length=50,
        verbose_name="Filial Telefon Nömrəsi",
        blank=True, null=True
    )
    work_days=models.CharField(
        max_length=250,
        verbose_name="İş Günü",
        blank=True, null=True,
        default="Bazar ertəsi – Cümə: 08:30 – 20:00"
    )
    map_embed = models.TextField(
        verbose_name="Google Maps Embed URL / iframe",
        blank=True, null=True,
        help_text="Bütün iframe kodunu və ya embed linkini buraya yapışdırın"
    )

    class Meta:
        verbose_name = "Əlaqə Məlumatı"
        verbose_name_plural = "Əlaqə Məlumatları"

    def __str__(self):
        return f"{self.phone or ''} | {self.email or ''}".strip(" |")


class FooterInfo(models.Model):
    title=models.TextField(
        verbose_name="Footer Təsviri",
        blank=True, null=True,
        default="Bizimlə Əlaqə Saxlayın"
    )
    description=models.TextField(
        verbose_name="Footer Təsvir",
        blank=True, null=True
    )
    copyright_text=models.CharField(
            max_length=200,
            verbose_name="Footer Mətni",
            blank=True, null=True
        )
    rights_reserved=models.CharField(
            max_length=100,
            verbose_name="Hüquqlar Mətni",
            blank=True, null=True,
            default="Bütün Hüquqlar Qorunur"
        )
    creation_text=models.CharField(
            max_length=100,
            verbose_name="Yaradıcı Mətn",
            blank=True, null=True
        )
    creation_url = models.URLField(
        verbose_name="Yaradıcı Link",
        blank=True, null=True,
        default="https://vrproduction.az/"
    )

    class Meta:
        verbose_name = "Footer Məlumatı"
        verbose_name_plural = "Footer Məlumatları"

    def __str__(self):
        return f"Footer Info: {self.title[:30]}..."




class PageType(models.TextChoices):
    HOME = 'home', 'Ana Səhifə'
    ABOUT = 'about', 'Haqqımızda'
    SERVICES = 'services', 'Xidmətlər (Siyahı Səhifəsi)'
    BLOG = 'blog', 'Blog (Siyahı Səhifəsi)'
    CONTACT = 'contact', 'Əlaqə'

class PageSEO(models.Model):
    page_type = models.CharField(
        max_length=50,
        choices=PageType.choices,
        unique=True,
    )

    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)

    og_image = models.ImageField(upload_to="seo/og-images/", blank=True, null=True)
    logo = models.ImageField(upload_to="seo/logos/", blank=True, null=True)
    canonical_url = models.URLField(blank=True, null=True)
    no_index = models.BooleanField(default=False)
    no_follow = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Səhifə SEO'
        verbose_name_plural = 'Səhifələr üçün SEO'

    def __str__(self):
        return f"{self.get_page_type_display()}"

    @staticmethod
    def get_seo(page_type):
        cache_key = f"seo_{page_type}"
        seo = cache.get(cache_key)

        if not seo:
            try:
                seo = PageSEO.objects.get(page_type=page_type)
            except PageSEO.DoesNotExist:
                seo = None

            cache.set(cache_key, seo, 60 * 60)

        return seo
