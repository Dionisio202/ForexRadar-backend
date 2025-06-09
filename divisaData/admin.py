from django.contrib import admin
from django.db.models import Min, Max, Count
from .models import ForexData, Divisa, UserDivisa

@admin.register(ForexData)
class ForexDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'frequency', 'min_date', 'max_date', 'num_registros')
    search_fields = ('symbol',)
    list_filter = ('frequency', 'symbol')

    def min_date(self, obj):
        # La fecha mínima que tienes para este symbol + frequency
        return ForexData.objects.filter(symbol=obj.symbol, frequency=obj.frequency).aggregate(Min('date'))['date__min']

    def max_date(self, obj):
        # La fecha máxima que tienes para este symbol + frequency
        return ForexData.objects.filter(symbol=obj.symbol, frequency=obj.frequency).aggregate(Max('date'))['date__max']

    def num_registros(self, obj):
        # Total de registros que tienes para este symbol + frequency
        return ForexData.objects.filter(symbol=obj.symbol, frequency=obj.frequency).count()

    # Para que aparezcan bien las columnas
    min_date.admin_order_field = 'date'
    max_date.admin_order_field = 'date'

@admin.register(Divisa)
class DivisaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'simbolo', 'imagen1', 'imagen2')
    search_fields = ('nombre', 'simbolo')

@admin.register(UserDivisa)
class UserDivisaAdmin(admin.ModelAdmin):
    list_display = ('user', 'divisa')
    search_fields = ('user__username', 'divisa__nombre')
