from django.urls import resolve, Resolver404
from .models import PageSEO, SiteLogo, SocialLink, ContactInfo, FooterInfo

def site_context(request):
    page_type = 'custom'

    # Default SEO dəyərləri (sabit, modeldən çəkilmir)
    seo_data = {
        'seo_title': 'Alisa Club | Uşaqlar üçün Tədbirlər və İnkişaf Klubu',
        'seo_description': 'Alisa Club — uşaqlar üçün maraqlı tədbirlər, yaradıcı oyunlar və inkişaf proqramları. Tədbir rezervasiyası, üzvlük sistemi və doğum günü planlayıcısı bir yerdə.',
        'meta_keywords': 'Alisa Club, uşaq klubu, tədbir, uşaqlar üçün oyun, doğum günü, uşaq inkişafı, valideyn klubu, Alisa, kreativ uşaq fəaliyyətləri, ailə tədbirləri',
        'og_title': 'Alisa Club | Tədbir və İnkişaf Klubu',
        'og_description': 'Uşaqlar üçün sevinc dolu tədbirlər, oyunlar və öyrədici fəaliyyətlər! Alisa Club — hər gün öyrənmək və əylənmək üçün ideal məkandır.',
        'og_image': None,

        'logo': None,
        'canonical_url': request.build_absolute_uri(),
        'no_index': False,
        'no_follow': False,
    }

    try:
        match = resolve(request.path_info)
        view_name = match.view_name or ''

        # Sənin URL adlarına əsasən səhifə tipləri
        if view_name in ['home', 'about', 'contact']:
            page_type = view_name

        elif view_name == 'blog':
            page_type = 'blog'
            seo_data.update({
                'seo_title': f"Blog | {seo_data['seo_title']}",
                'seo_description': f"Explore our latest blog posts | {seo_data['seo_description']}",
                'og_title': 'Blog',
                'og_description': 'Explore our latest blog posts',
            })

        elif view_name == 'services':
            page_type = 'services'
            seo = PageSEO.get_seo(page_type='services')
            default_title = f"Services | {seo_data['seo_title']}"
            default_description = f"Explore our professional services | {seo_data['seo_description']}"
            seo_data.update({
                'seo_title': seo.seo_title if seo and seo.seo_title else default_title,
                'seo_description': seo.seo_description if seo and seo.seo_description else default_description,
                'og_title': seo.og_title if seo and seo.og_title else 'Services',
                'og_description': seo.og_description if seo and seo.og_description else default_description,
                'og_image': seo.og_image.url if seo and seo.og_image else None,
                'logo': seo.logo.url if seo and seo.logo else None,
                'canonical_url': seo.canonical_url if seo and seo.canonical_url else request.build_absolute_uri(),
                'no_index': seo.no_index if seo else False,
                'no_follow': seo.no_follow if seo else False,
            })

        # PageSEO modelindən əlavə SEO məlumatları
        seo = PageSEO.get_seo(page_type=page_type)
        if seo:
            seo_data.update({
                'seo_title': seo.seo_title or seo_data['seo_title'],
                'seo_description': seo.seo_description or seo_data['seo_description'],
                'meta_keywords': seo.meta_keywords or seo_data['meta_keywords'],
                'og_title': seo.og_title or seo_data['og_title'],
                'og_description': seo.og_description or seo_data['og_description'],
                'og_image': seo.og_image.url if seo.og_image else seo_data['og_image'],
                'logo': seo.logo.url if seo.logo else seo_data['logo'],
                'canonical_url': seo.canonical_url or seo_data['canonical_url'],
                'no_index': seo.no_index,
                'no_follow': seo.no_follow,
            })

    except Resolver404:
        pass

    # Absolute og_image URL yarat
    if seo_data['og_image']:
        seo_data['og_image'] = request.build_absolute_uri(seo_data['og_image'])

    return {
        'seo_data': seo_data,
        'page_type': page_type,
    }


def global_context(request):
    from django.utils import timezone
    from apps.blog.models import Event, Blog

    # Sabit məlumatlar
    social_links = SocialLink.objects.first()
    logo = SiteLogo.objects.first()
    contact = ContactInfo.objects.first()
    footer = FooterInfo.objects.first()
    
    # Upcoming events for sidebar (3 events)
    upcoming_events = Event.objects.filter(
        is_active=True
    ).order_by('-event_date')[:3]
    
    # Footer event (only one event with show_in_footer=True)
    footer_event = Event.objects.filter(
        is_active=True,
        show_in_footer=True
    ).order_by('-event_date').first()
    
    # Sidebar blogs (3 recent blogs with show_in_sidebar=True)
    sidebar_blogs = Blog.objects.filter(
        is_active=True,
        show_in_sidebar=True
    ).order_by('sidebar_order', '-date')[:3]

    return {
        'social_links': social_links,
        'logo': logo,
        'contact': contact,
        'footer': footer,
        'upcoming_events': upcoming_events,
        'footer_event': footer_event,
        'sidebar_blogs': sidebar_blogs,
    }
