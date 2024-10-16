
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include('Account.api.urls')),
    path("api/", include('Store.api.urls')),
    path("api/", include('Cart.api.urls')),
    path("api/", include('Order.api.urls')),
    path('api/', include('Coupon.api.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

