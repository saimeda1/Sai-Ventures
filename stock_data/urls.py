# In sai_ventures/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from stock_data.views import HistoricalDataViewSet

router = routers.DefaultRouter()
router.register(r'historical-data', HistoricalDataViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
