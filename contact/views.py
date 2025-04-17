from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Contact
from .forms import ContactForm


def email_confirm(request):
    """ A view to display the email confirmation page """
    return render(request, 'contact/email-confirm.html')


def contact(request):
    """ A view to return the contact page """
    contact_form = ContactForm(request.POST or None)
    if request.method == "POST":
        if contact_form.is_valid():
            contact_form.save()

            # Send confirmation email
            subject = "Thank you for contacting Megan Roberts Dressage."
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [request.POST.get('email'), ]

            # Prepare the HTML content for the email
            html_content = render_to_string('contact/email-confirm.html', {
                'user_name': request.POST.get('first_name'),
            })

            # Send email
            send_mail(
                subject,
                '',
                from_email,
                to_email,
                html_message=html_content
            )

            # Show success message
            messages.info(
                request,
                "Thank you! Your email was successful. "
                "You will receive a confirmation email soon. Meg x"
            )

            return redirect(reverse('email-confirm'))

        messages.error(request, "Error, please try again.")

    template = "contact/contact.html"
    context = {
        "contact_form": contact_form,
    }
    return render(request, template, context)
