from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from apps.birthday.models import BirthdayPageSettings, BirthdayGallery, BirthdayReservation
from apps.home.models import BirthdayReservationSettings


def birthday(request):
    page_settings = BirthdayPageSettings.objects.filter(is_active=True).first()
    galleries = BirthdayGallery.objects.filter(is_active=True).order_by('order')
    reservation_settings = BirthdayReservationSettings.objects.filter(is_active=True).first()
    
    # Handle form submission
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
            return redirect('birthday')
        except Exception as e:
            messages.error(request, 'Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.')
    
    context = {
        'page_settings': page_settings,
        'galleries': galleries,
        'reservation_settings': reservation_settings,
        'today': date.today().isoformat(),
    }
    return render(request, 'pages/birthday/birthday.html', context)
