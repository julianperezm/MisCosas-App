from django.contrib import admin

from .models import Item, Alimentador, Users, Voto, Comentario

admin.site.register(Item)
admin.site.register(Alimentador)
admin.site.register(Users)
admin.site.register(Voto)
admin.site.register(Comentario)
