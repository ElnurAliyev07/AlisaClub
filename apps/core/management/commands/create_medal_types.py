from django.core.management.base import BaseCommand
from apps.core.models_profile import MedalType

class Command(BaseCommand):
    help = 'Default medal növlərini yaradır'

    def handle(self, *args, **kwargs):
        medals = [
            {'name': 'Yaradıcılıq', 'icon': '🎨', 'description': 'Rəsm və yaradıcılıq tədbirlərində iştirak'},
            {'name': 'Aktiv İştirakçı', 'icon': '🤸', 'description': 'Fiziki fəaliyyət və idman tədbirlərində iştirak'},
            {'name': 'Əyləncə Ustası', 'icon': '🎭', 'description': 'Əyləncə və oyun tədbirlərində iştirak'},
            {'name': 'Elm Həvəskarı', 'icon': '🔬', 'description': 'Elm və texnologiya tədbirlərində iştirak'},
            {'name': 'Musiqi Sevən', 'icon': '🎵', 'description': 'Musiqi və rəqs tədbirlərində iştirak'},
            {'name': 'Doğum Günü Qəhrəmanı', 'icon': '🎂', 'description': 'Doğum günü tədbirində iştirak'},
            {'name': 'Komanda Oyunçusu', 'icon': '🤝', 'description': 'Komanda oyunlarında iştirak'},
            {'name': 'Ulduz İştirakçı', 'icon': '⭐', 'description': 'Xüsusi tədbirdə iştirak'},
        ]
        
        created_count = 0
        for medal_data in medals:
            medal, created = MedalType.objects.get_or_create(
                name=medal_data['name'],
                defaults={
                    'icon': medal_data['icon'],
                    'description': medal_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ {medal.icon} {medal.name} yaradıldı'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ {medal.icon} {medal.name} artıq mövcuddur'))
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 {created_count} yeni medal növü yaradıldı!'))
