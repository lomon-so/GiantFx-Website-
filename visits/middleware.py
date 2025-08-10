import datetime
from ip2geotools.databases.noncommercial import DbIpCity
from django.utils.timezone import now
from .models import Visit

class VisitTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.tracked_paths = ['/about/', '/mentorship/', '/signals/', '/payment/', '/contact/']
        # self.tracked_paths = ['/', '/signals/', '/mentorship/', '/contact/', '/payment/']

    def __call__(self, request):
        response = self.get_response(request)

        ip = self.get_client_ip(request)
        path = request.path
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Track selected paths
        if any(path.startswith(p) for p in self.tracked_paths):
            five_minutes_ago = now() - datetime.timedelta(minutes=5)
            recent_visit = Visit.objects.filter(ip_address=ip, path=path, timestamp__gte=five_minutes_ago).first()

            if not recent_visit:
                country, city = '', ''
                try:
                    geo = DbIpCity.get(ip, api_key='free')
                    country = geo.country
                    city = geo.city
                except Exception:
                    pass

                Visit.objects.create(
                    ip_address=ip,
                    user_agent=user_agent,
                    path=path,
                    country=country,
                    city=city
                )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
