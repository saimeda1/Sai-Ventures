# In stock_data/views.py
from rest_framework import viewsets
from .models import HistoricalData
from .serializers import HistoricalDataSerializer

class HistoricalDataViewSet(viewsets.ModelViewSet):
    queryset = HistoricalData.objects.all()
    serializer_class = HistoricalDataSerializer

# In stock_data/serializers.py
from rest_framework import serializers
from .models import HistoricalData

class HistoricalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalData
        fields = '__all__'
