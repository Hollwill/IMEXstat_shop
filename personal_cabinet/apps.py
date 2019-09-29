from django.apps import AppConfig


class PersonalCabinetConfig(AppConfig):
    name = 'personal_cabinet'
    verbose_name = 'Личный кабинет'

    def ready(self):
        import personal_cabinet.signals
