from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=input("Введите почту: "),
            first_name=input("Введите Имя: "),
            last_name=input("Введите Фамилию: "),
            is_staff=False,
            is_superuser=False
        )

        user.set_password('12345')
        user.save()
