from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from datetime import date
from apps.contact.models import Contact
from apps.home.models import (
    Hero, About, SessionTime, WhyChooseUs, KidContent, FAQ, 
    BirthdayEvent, BirthdayReservationSettings
)
from apps.blog.models import Blog, Event, HomePageBlogSettings
from apps.birthday.models import BirthdayReservation
from apps.core.models_profile import Medal, Discount
from apps.services.models import Service

def home(request):
    # Handle birthday reservation form submission
    if request.method == 'POST':
        try:
            reservation = BirthdayReservation(
                child_name=request.POST.get('child_name'),
                birth_date=request.POST.get('birth_date'),
                event_date=request.POST.get('event_date'),
                parent_name=request.POST.get('parent_name'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                participants=request.POST.get('participants'),
                notes=request.POST.get('notes'),
                subscribe_to_events=request.POST.get('subscribe_to_events') == 'on'
            )
            reservation.save()
            messages.success(request, '🎉 Rezervasiyanız uğurla qeydə alındı! Tezliklə sizinlə əlaqə saxlayacağıq.')
            return redirect('home')
        except Exception as e:
            messages.error(request, 'Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.')
    
    # Hero slaydı üçün məlumatlar (bütün tədbirlər - keçmiş və gələcək)
    hero_events = Event.objects.filter(
        is_active=True, 
        show_on_hero=True
    ).order_by('-event_date')[:5]  # Ən yeni tədbirlər əvvəl
    
    hero_campaigns = Discount.objects.filter(
        is_active=True,
        show_on_homepage=True,
        valid_from__lte=timezone.now().date(),
        valid_until__gte=timezone.now().date()
    ).order_by('-valid_from')[:3]
    
    about = About.objects.first()
    why_choose_us = WhyChooseUs.objects.filter(is_active=True).first()
    kid_content = KidContent.objects.filter(is_active=True).first()
    faq = FAQ.objects.filter(is_active=True).first()
    event = BirthdayEvent.objects.first()
    
    # Blog and Events for home page
    homepage_blogs = Blog.objects.filter(is_active=True, show_on_homepage=True).order_by('homepage_order', '-date')[:3]
    
    # Events for home page (bütün tədbirlər - keçmiş və gələcək)
    upcoming_events = Event.objects.filter(
        is_active=True, 
        show_on_homepage=True
    ).order_by('-event_date')[:6]  # Ən yeni tədbirlər əvvəl
    
    # Home page blog settings
    homepage_blog_settings = HomePageBlogSettings.objects.filter(is_active=True).first()
    
    # Reservation settings
    reservation_settings = BirthdayReservationSettings.objects.filter(is_active=True).first()
    
    # Medals - Ana səhifədə göstəriləcək medallar
    medals = Medal.objects.filter(show_on_homepage=True).select_related(
        'child', 'child__parent', 'child__parent__user', 'medal_type'
    ).order_by('-awarded_at')[:6]  # Son 6 medal
    
    # Campaigns - Aktiv kampaniyalar
    campaigns = Discount.objects.filter(
        is_active=True,
        show_on_homepage=True
    ).filter(
        valid_from__lte=timezone.now().date(),
        valid_until__gte=timezone.now().date()
    ).order_by('-valid_from')[:6]
    
    # Services - Ana səhifə üçün xidmətlər (standart xidmətlər)
    services = Service.objects.filter(is_active=True, show_in_standard=True).order_by('order')[:3]
    
    context = {
        'hero_events': hero_events,
        'hero_campaigns': hero_campaigns,
        'about': about,
        'session_times': SessionTime.objects.filter(about=about) if about else [],
        'why_choose_us': why_choose_us,
        'why_choose_us_items': why_choose_us.items.filter(is_active=True).order_by('order') if why_choose_us else [],
        'kid_content': kid_content,
        'kid_content_items': kid_content.items.filter(is_active=True).order_by('position', 'order') if kid_content else [],
        'faq': faq,
        'faq_items': faq.items.filter(is_active=True).order_by('order') if faq else [],
        'event': event,
        'features': event.features.all() if event else [],
        'homepage_blogs': homepage_blogs,
        'homepage_blog_settings': homepage_blog_settings,
        'upcoming_events': upcoming_events,
        'reservation_settings': reservation_settings,
        'medals': medals,
        'campaigns': campaigns,
        'services': services,
        'today': date.today().isoformat(),
    }
    return render(request, 'pages/home/home.html', context)

def contact(request):
    from django.contrib import messages
    from apps.contact.models import ContactMessage
    
    contact_info = Contact.objects.first()
    
    # Handle form submission
    if request.method == 'POST':
        try:
            contact_message = ContactMessage(
                first_name=request.POST.get('firstname', ''),
                last_name=request.POST.get('lastname', ''),
                email=request.POST.get('email', ''),
                phone=request.POST.get('number', ''),
                message=request.POST.get('message', '')
            )
            contact_message.save()
            messages.success(request, 'Mesajınız uğurla göndərildi! Tezliklə sizinlə əlaqə saxlayacağıq.')
        except Exception as e:
            messages.error(request, 'Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.')
    
    context = {
        'contact_info': contact_info,
    }
    return render(request, 'pages/home/contact.html', context)

def about(request):
    from apps.about.models import (
        AboutPageSettings, AboutSection, Timeline, TimelineSettings,
        Gallery, GallerySettings
    )
    
    page_settings = AboutPageSettings.objects.filter(is_active=True).first()
    about_sections = AboutSection.objects.filter(is_active=True).order_by('order')
    timeline_settings = TimelineSettings.objects.filter(is_active=True).first()
    timelines = Timeline.objects.filter(is_active=True).order_by('order', 'year')
    gallery_settings = GallerySettings.objects.filter(is_active=True).first()
    galleries = Gallery.objects.filter(is_active=True).order_by('order')
    
    # Keep existing data for includes
    kid_content = KidContent.objects.filter(is_active=True).first()
    faq = FAQ.objects.filter(is_active=True).first()
    
    context = {
        'page_settings': page_settings,
        'about_sections': about_sections,
        'timeline_settings': timeline_settings,
        'timelines': timelines,
        'gallery_settings': gallery_settings,
        'galleries': galleries,
        'kid_content': kid_content,
        'kid_content_items': kid_content.items.filter(is_active=True).order_by('position', 'order') if kid_content else [],
        'faq': faq,
        'faq_items': faq.items.filter(is_active=True).order_by('order') if faq else []
    }
    return render(request, 'pages/about/about.html', context)

def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)