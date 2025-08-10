from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Contact Messages
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-date_sent']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'


# Newsletter Subscribers
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'


# Product & Pricing Choices
PRODUCT_CHOICES = [
    ('signal_monthly', 'Monthly Signal'),
    ('signal_yearly', 'Yearly Signal'),
    ('signal_lifetime', 'Lifetime Signal'),
    ('mentorship_online', 'Online Mentorship'),
    ('mentorship_physical', 'Physical Mentorship'),
    ('mentorship_private', 'Private Mentorship'),
]

SIGNAL_PRICING = {
    'signal_monthly': 50,
    'signal_yearly': 250,
    'signal_lifetime': 500,
}

MENTORSHIP_PRICING = {
    'mentorship_online': 199,
    'mentorship_physical': 299,
    'mentorship_private': 599,
}


# Payment Model
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bank', 'Bank Transfer'),
        ('crypto', 'Crypto'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField(region='NG')
    product_type = models.CharField(max_length=50, choices=PRODUCT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.product_type} - {self.status}"

    class Meta:
        ordering = ['-paid_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'




