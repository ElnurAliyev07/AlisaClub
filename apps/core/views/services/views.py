from django.shortcuts import render, get_object_or_404
from apps.services.models import ServicePageSettings, Service


def service(request):
    from apps.home.models import WhyChooseUs
    
    page_settings = ServicePageSettings.objects.filter(is_active=True).first()
    
    # Get services by display options
    featured_services = Service.objects.filter(is_active=True, show_in_featured=True).order_by('order')
    standard_services = Service.objects.filter(is_active=True, show_in_standard=True).order_by('order')
    
    # Get "Why Choose Us" from home app
    why_choose_us = WhyChooseUs.objects.filter(is_active=True).prefetch_related('items').first()
    
    context = {
        'page_settings': page_settings,
        'featured_services': featured_services,
        'standard_services': standard_services,
        'why_choose_us': why_choose_us,
    }
    return render(request, 'pages/services/service.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    # Get related data
    features = service.features.all().order_by('order')
    schedules = service.schedules.all().order_by('order')
    faqs = service.faqs.filter(is_active=True).order_by('order')
    
    context = {
        'service': service,
        'features': features,
        'schedules': schedules,
        'faqs': faqs,
    }
    return render(request, 'pages/services/service-detail.html', context)
