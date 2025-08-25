from django.contrib import admin
from .models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        'ip_address',
        'path',
        'city',
        'country',
        'user_agent_display',
        'timestamp',
    )
    list_filter = ('timestamp', 'country', 'city')
    search_fields = ('ip_address', 'path', 'user_agent', 'city', 'country')
    readonly_fields = ('ip_address', 'path', 'city', 'country', 'user_agent', 'timestamp')

    def user_agent_display(self, obj):
        if obj.user_agent:
            return obj.user_agent[:50] + "..." if len(obj.user_agent) > 50 else obj.user_agent
        return "(no user agent)"
    
    user_agent_display.short_description = "User Agent"
