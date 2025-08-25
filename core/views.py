from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives  
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import ContactForm, NewsletterForm, PaymentForm, Payment
from .models import Payment, PRODUCT_CHOICES, SIGNAL_PRICING, MENTORSHIP_PRICING

pricing_map = {**SIGNAL_PRICING, **MENTORSHIP_PRICING}



# Create your views here.

# FUNCTIONS FOR TEMPLATES
def home(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def packages(request):
    return render(request, 'core/courses.html')

def team(request):
    return render(request, 'core/team.html')

def testimonial(request):
    return render(request, 'core/testimonial.html')

def sandra(request):
    return render(request, 'core/sandra.html')



# FUNCTION FOR CONTACT-MESSAGE

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Send email to admin
            admin_subject = f"New Contact Message from {contact.name}"
            admin_text = f"Subject: {contact.subject}\n\nMessage:\n{contact.message}\n\nFrom: {contact.name} <{contact.email}>"
            admin_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>📩 New Contact Submission</h2>
                <p><strong>Name:</strong> {contact.name}</p>
                <p><strong>Email:</strong> {contact.email}</p>
                <p><strong>Subject:</strong> {contact.subject}</p>
                <p><strong>Message:</strong><br>{contact.message}</p>
            </body>
            </html>
            """
            admin_msg = EmailMultiAlternatives(admin_subject, admin_text, settings.EMAIL_HOST_USER, ['lomonsofx@gmail.com'])
            admin_msg.attach_alternative(admin_html, "text/html")
            admin_msg.send()

            # Send confirmation email to sender
            user_subject = "Thanks for contacting Giant Fx"
            user_text = f"""
            Hi {contact.name},
            
            Thanks for reaching out to Giant Fx. We’ve received your message and will get back to you shortly.
            
            If your matter is urgent, reply to this email.
            
            -- Giant Fx Team
            """
            user_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                <table style="max-width: 600px; margin: auto; background: white; border-radius: 8px; overflow: hidden; border: 1px solid #eee;">
                    <tr style="background-color: #ff6600; color: white;">
                        <td style="padding: 20px; text-align: center; font-size: 20px;">
                            <strong>Giant Fx</strong>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 20px; color: #333;">
                            <p>Hi <strong>{contact.name}</strong>,</p>
                            <p>Thanks for getting in touch with <strong>Giant Fx</strong>. We’ve successfully received your message.</p>
                            <p>One of our support team members will review your inquiry and get back to you as soon as possible.</p>
                            <p>If your matter is urgent, you can reply directly to this email for faster assistance.</p>
                            <p style="margin-top: 20px;">Best regards,<br><strong>The Giant Fx Team</strong></p>
                        </td>
                    </tr>
                    <tr style="background-color: #f4f4f4;">
                        <td style="padding: 10px; font-size: 12px; text-align: center; color: #777;">
                            This is an automated confirmation from Giant Fx. Please do not share sensitive information via email.
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
            user_msg = EmailMultiAlternatives(user_subject, user_text, settings.EMAIL_HOST_USER, [contact.email])
            user_msg.attach_alternative(user_html, "text/html")
            user_msg.send()

            messages.success(request, 'Your message was sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            messages.success(request, 'Subscribed successfully!')

            # Confirmation email to subscriber
            subject = "Thanks for subscribing to Giant Fx!"
            text_content = """
            Hi there!
            
            You’re now on our newsletter list. Expect trading tips, psychology boosts, and market insights.
            
            If this wasn’t you, just ignore this email.
            """
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                <table style="max-width: 600px; margin: auto; background: white; border-radius: 8px; overflow: hidden; border: 1px solid #eee;">
                    <tr style="background-color: #ff6600; color: white;">
                        <td style="padding: 20px; text-align: center; font-size: 20px;">
                            <strong>Giant Fx Newsletter</strong>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 20px; color: #333;">
                            <p>Hi there!</p>
                            <p>You’re now subscribed to the <strong>Giant Fx</strong> newsletter. Expect:</p>
                            <ul>
                                <li>💡 Trading tips</li>
                                <li>🧠 Psychology boosts</li>
                                <li>📊 Market insights</li>
                            </ul>
                            <p>We’re excited to have you on board!</p>
                        </td>
                    </tr>
                    <tr style="background-color: #f4f4f4;">
                        <td style="padding: 10px; font-size: 12px; text-align: center; color: #777;">
                            This is an automated email from Giant Fx. You can unsubscribe anytime by replying with "Unsubscribe".
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [subscriber.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        else:
            messages.error(request, 'This email is already subscribed.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))





def payment(request):
    product_type = request.GET.get('product', '')
    product_name = dict(PRODUCT_CHOICES).get(product_type, 'Invalid Product')
    amount = SIGNAL_PRICING.get(product_type) or MENTORSHIP_PRICING.get(product_type)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, "Payment info submitted successfully. Please follow the next instructions.")
            return redirect('payment_confirmation', payment_id=payment.id)
        else:
            messages.error(request, "Form submission failed. Please correct the errors.")
    else:
        form = PaymentForm(initial={
            'product_type': product_type,
            'amount': amount
        })

    return render(request, 'core/payment.html', {
        'form': form,
        'product_name': product_name,
        'amount': amount,
    })


def payment_confirmation(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'core/payment_confirmation.html', {
        'payment': payment
    })

