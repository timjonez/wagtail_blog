from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from .forms import ContactForm

# Create your views here.

@login_required
def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = 'contactus@jonezfam.com'
            message = form.cleaned_data['from_email']+' '+form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['timjonez@protonmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('home')
    return render(request, "contact_us/contact.html", {'form': form})

def successView(request):
    return redirect("home")

