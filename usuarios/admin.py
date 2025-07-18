from django.contrib import admin
from .models import Nota
# Register your models here.

admin.site.register(Nota)  # Registra o modelo Nota no admin do Django
# Isso permite que você gerencie as notas através da interface administrativa do Django.