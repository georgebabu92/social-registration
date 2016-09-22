from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from login.forms import LoginForm
from login.views import register, ProfileView, login
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register, name='register'),
    url(r'^profile/', ProfileView.as_view(), name='profile'),
    url(r'^$', login, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

