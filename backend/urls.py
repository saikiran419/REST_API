from django.contrib import admin
from django.urls import path, include  # ✅ correct import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('lms.urls')),  # ✅ include the module, NOT the urlpatterns list
]