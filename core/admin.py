from django.contrib.auth.models import Group
from django.contrib import admin
from .models import Payment, ContactMessage, NewsletterSubscriber
from django.http import HttpResponse
import csv


admin.site.unregister(Group)

# === CSV EXPORT UTIL ===
def export_as_csv(modeladmin, request, queryset):
    model = modeladmin.model
    meta = model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.model_name}s.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = [getattr(obj, field) if not callable(getattr(obj, field)) else '' for field in field_names]
        writer.writerow(row)

    return response

export_as_csv.short_description = "Export Selected as CSV"

# === PAYMENT ADMIN ===
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'phone', 'product_type',
        'amount', 'payment_method', 'status', 'paid_at'
    )
    list_filter = ('product_type', 'payment_method', 'status', 'paid_at')
    search_fields = ('name', 'email', 'phone', 'product_type')
    ordering = ['-paid_at']
    list_editable = ('status',)
    readonly_fields = (
        'name', 'email', 'phone', 'product_type',
        'amount', 'payment_method', 'paid_at'
    )
    actions = [export_as_csv]

    fieldsets = (
        ('Payment Info', {
            'fields': (
                'name', 'email', 'phone',
                'product_type', 'amount',
                'payment_method', 'status', 'paid_at'
            )
        }),
    )

# === CONTACT MESSAGE ADMIN ===
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_sent')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('date_sent',)
    ordering = ['-date_sent']
    readonly_fields = ('name', 'email', 'subject', 'message', 'date_sent')
    actions = [export_as_csv]

# === NEWSLETTER SUBSCRIBER ADMIN ===
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    list_filter = ('subscribed_at',)
    ordering = ['-subscribed_at']
    readonly_fields = ('email', 'subscribed_at')
    actions = [export_as_csv]






