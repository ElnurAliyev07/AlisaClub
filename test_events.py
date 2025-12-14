import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.blog.models import Event
from django.utils import timezone

print("=" * 50)
print("TƏDBIR YOXLANIŞI")
print("=" * 50)

# Bütün tədbirlər
all_events = Event.objects.all()
print(f"\n📊 Ümumi tədbir sayı: {all_events.count()}")

# Aktiv tədbirlər
active_events = Event.objects.filter(is_active=True)
print(f"✅ Aktiv tədbir sayı: {active_events.count()}")

# Ana səhifədə göstərilən tədbirlər
homepage_events = Event.objects.filter(is_active=True, show_on_homepage=True)
print(f"🏠 Ana səhifədə göstərilən: {homepage_events.count()}")

# Hero-da göstərilən tədbirlər
hero_events = Event.objects.filter(is_active=True, show_on_hero=True)
print(f"🎯 Hero-da göstərilən: {hero_events.count()}")

# Footer-də göstərilən tədbirlər
footer_events = Event.objects.filter(is_active=True, show_in_footer=True)
print(f"📍 Footer-də göstərilən: {footer_events.count()}")

print("\n" + "=" * 50)
print("TƏDBIR DETALLARI")
print("=" * 50)

for event in all_events:
    print(f"\n📅 {event.title}")
    print(f"   Tarix: {event.event_date}")
    print(f"   Aktiv: {'✅' if event.is_active else '❌'}")
    print(f"   Ana səhifə: {'✅' if event.show_on_homepage else '❌'}")
    print(f"   Hero: {'✅' if event.show_on_hero else '❌'}")
    print(f"   Footer: {'✅' if event.show_in_footer else '❌'}")
    
    # Gələcək tarixdirmi?
    if event.event_date:
        is_future = event.event_date >= timezone.now()
        print(f"   Gələcək tarix: {'✅' if is_future else '❌ (Keçmiş tarix!)'}")

print("\n" + "=" * 50)
