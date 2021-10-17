from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('profile/', include('profile_app.urls')),
    path('payment/', include('payment.urls')),
]
