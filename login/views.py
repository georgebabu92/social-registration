from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from .models import User
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProfileImage
from .forms import ProfileForm
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import login as django_login


def login(request):
    data = {'template_name': 'registration/login.html', 'authentication_form': LoginForm}
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')
    else:
        return django_login(request, **data)


def home(request):
    if not request.user.is_authenticated():
        return redirect('/')
    return render_to_response('home.html', {'user': request.user})


def register(request):
    form = RegistrationForm
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')
    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username'])
                # TODO raise error user already exists
            except:
                user = User.objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    email=form.cleaned_data['email']
                )
                user.save()
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                if user is not None:
                    login(request, user)
                return HttpResponseRedirect('/profile')
        else:
            form = RegistrationForm
    return render(request, 'registration/register.html', {'form': form})


class ProfileView(FormView):
    template_name = 'registration/profile.html'
    form_class = ProfileImageForm
    success_url = '/profile/'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user_image = ProfileImage.objects.filter(user=self.request.user)
        if user_image:
            try:
                context['url'] = user_image[0].image.url
            except ValueError:
                pass
        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(ProfileView, self).get_initial()

        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):

        user = User.objects.get(pk=self.request.user.pk)
        try:
            user_image = ProfileImage.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            user_image = ProfileImage(user=self.request.user)

        user_image.image = form.cleaned_data['image']
        user_image.save()
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        return HttpResponseRedirect(self.get_success_url())




