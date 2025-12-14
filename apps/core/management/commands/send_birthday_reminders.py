from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from apps.core.models_profile import Child

class Command(BaseCommand):
    help = 'Doğum günü yaxınlaşan uşaqların valideynlərinə e-mail göndərir'

    def handle(self, *args, **kwargs):
        children_with_upcoming_birthdays = []
        
        for child in Child.objects.select_related('parent__user').all():
            if child.is_birthday_soon(days=14):
                children_with_upcoming_birthdays.append(child)
        
        if not children_with_upcoming_birthdays:
            self.stdout.write(self.style.WARNING('⚠️ Yaxın zamanda doğum günü olan uşaq tapılmadı.'))
            return
        
        sent_count = 0
        for child in children_with_upcoming_birthdays:
            parent = child.parent
            user = parent.user
            
            if not user.email:
                self.stdout.write(self.style.WARNING(f'⚠️ {user.get_full_name()} üçün e-mail ünvanı yoxdur'))
                continue
            
            subject = f'🎂 {child.name}-in doğum günü yaxınlaşır!'
            message = f"""
Hörmətli {user.get_full_name()},

{child.name}-in doğum günü yaxınlaşır! ({child.birth_date.strftime('%d.%m.%Y')})

Xüsusi doğum günü tədbiri endirimindən yararlanın və uşağınız üçün unudulmaz bir gün yaradın.

Profil səhifənizdən tədbir rezervasiyası edə bilərsiniz.

Hörmətlə,
Alisa Club
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                sent_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ {user.email} - {child.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Xəta: {user.email} - {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 {sent_count} e-mail göndərildi!'))
