from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import forms
from . import models
# Create your views here.

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

class SignUp(CreateView):
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


def custom_signup(request):
    if request.method == 'POST':
        invitation = False
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            model = models.InviteCodeModel.objects.all()
            print('IS VALID')
            print(model[0])
            invite_code = form.cleaned_data.get('invite_code')
            print('invite code: '+invite_code)

            for item in model:
                print('FORLOOP')
                print(item)
                if str(item) == str(invite_code):
                    invitation = True
                    print('FOUND')
                    form.save()
                    email = form.cleaned_data.get('email')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(email=email, password=raw_password)
                    login(request, user)
                    return redirect('login')
            else:
                print('Failed forloop')
                messages.error(request, 'Invitation code is not valid')

    else:
        form = forms.CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


class EmailOpt(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    slug_field = 'email'
    model = models.CustomUser
    fields = ['email_update',]
    template_name = 'users/user_change.html'
    success_url = '/'
    

    def get_queryset(self):
        user = get_object_or_404(models.CustomUser, email=self.kwargs['slug'] )
        print(user)
        return models.CustomUser.objects.all()

    def test_func(self):
        user = get_object_or_404(models.CustomUser, email=self.kwargs['slug'] )
        return self.request.user == user