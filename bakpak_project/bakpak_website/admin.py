from django.contrib import admin
from .models import NewsletterDB, CoordinatesMapDB
from django.http import HttpResponse
import csv

# Register your models here

class InfoColumnGPS(admin.ModelAdmin):
    list_display = ['name_of_locations', 'adresse', 'code_postal', 'localite']

def export_to_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for emails in queryset:
        row = writer.writerow([getattr(emails, field) for field in field_names])

    export_to_csv.short_description = "Export to CSV"
    return response


class ExportNewsletter(admin.ModelAdmin):
    list_display = ["email"]
    actions = [export_to_csv]


admin.site.register(NewsletterDB, ExportNewsletter)
admin.site.register(CoordinatesMapDB, InfoColumnGPS)

