
from rest_framework.serializers import ModelSerializer


from .models import Event

class EventModelSerializer(ModelSerializer):

   class Meta:
       model = Event
       fields = ('date', 'views', 'clicks', 'costs')


