from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Company
from django.db import transaction

class Command(BaseCommand):
    help = 'Sets up guest access with Pruevas company'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create or get Pruevas company
            pruevas_company, created = Company.objects.get_or_create(
                name="Pruevas",
                defaults={
                    'description': 'Empresa de demostración',
                    'address': 'Calle Demo 123',
                    'phone': '123456789',
                    'email': 'demo@pruevas.com'
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Creada empresa 'Pruevas'"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Empresa 'Pruevas' ya existe"))
            
            # Create or get guest user
            guest_user, user_created = User.objects.get_or_create(
                username='guest',
                defaults={
                    'email': 'guest@example.com',
                    'is_staff': False,
                    'is_superuser': False,
                    'first_name': 'Usuario',
                    'last_name': 'Invitado'
                }
            )
            
            if user_created:
                guest_user.set_unusable_password()
                guest_user.save()
                self.stdout.write(self.style.SUCCESS(f"Creado usuario 'guest'"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Usuario 'guest' ya existe"))
            
            # Ensure user has profile and can access Pruevas
            if hasattr(guest_user, 'profile'):
                if not guest_user.profile.authorized_companies.filter(pk=pruevas_company.id).exists():
                    guest_user.profile.authorized_companies.add(pruevas_company)
                    self.stdout.write(self.style.SUCCESS(f"Acceso a 'Pruevas' otorgado a usuario 'guest'"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Usuario 'guest' ya tiene acceso a 'Pruevas'"))
            else:
                self.stdout.write(self.style.ERROR(f"El usuario 'guest' no tiene perfil asociado"))
                
        self.stdout.write(self.style.SUCCESS(f"Configuración completada. Los usuarios anónimos ahora pueden acceder como invitados."))
