from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import logout_user 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('logout/', logout_user, name='logout'),
    path('services/', include('services.urls')),
    path('contact/', include('contact.urls')),
    path('accounts/', include('allauth.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
]
