from django.core.management.base import BaseCommand

from api.models import Award

class Command(BaseCommand):
    help = "Добавляем стандартные данные в админку"

    def handle(self, *args, **options):
        awards = [
            Award(
                name="Энтузиаст",
                description="Выполнил 5 сложных задач",
                max_progress=5,
                type="Enthusiast"
            ),
            Award(
                name="Сама пунктуальность",
                description="Выполнил 15 задач в срок",
                max_progress=15,
                type="Punctuality"
            ),
            Award(
                name="Охотник",
                description="Завершил 20 лёгких задач в срок",
                max_progress=20,
                type="Hunter"
            ),
            Award(
                name="Тише едешь - дальше будешь",
                description="Выполнил 3 задачи сроком более 15 дней",
                max_progress=3,
                type="Easy_does_it"
            ),
        ]

        for award in awards:
            award.save()
