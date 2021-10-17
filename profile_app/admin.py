from django.contrib import admin
from .models import Package,Fund,Fundrecord,Roiincome,LevelIncome,SupportTicket
# Register your models here.

class PackageAdmin(Package):
    list_display = ('amount', 'days', 'max_profit', 'is_active',)
    search_fields = ('amount', 'max_profit',)
    readonly_fields = ('amount',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Package)
admin.site.register(Fund)
admin.site.register(Fundrecord)
admin.site.register(Roiincome)
admin.site.register(LevelIncome)
admin.site.register(SupportTicket)