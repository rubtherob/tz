
from rest_framework import status
from rest_framework.response import Response
from decimal import Decimal, ROUND_05UP

from rest_framework.viewsets import ModelViewSet

from event.filter import EventFilter
from event.models import Event
from event.serializers import EventModelSerializer



class EventViewset(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer
    filterset_class = EventFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if self.request.query_params:
            serializer = self.get_serializer(queryset, many=True)
            for data in serializer.data:
                data.update({'cpc':Decimal(data['costs'])/Decimal(data['clicks'])})
                data['cpc'] = data['cpc'].quantize(Decimal("1.00") , ROUND_05UP)
                data.update({'cpm': Decimal(data['costs']) / Decimal(data['views']) * 1000})
                data['cpm'] = data['cpm'].quantize(Decimal("1.00"), ROUND_05UP)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(many=True)
            return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if Event.objects.filter(date=request.data['date']).exists():
            event = Event.objects.get(date=request.data['date'])
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            event.views += serializer.data['views']
            event.clicks += serializer.data['clicks']
            event.costs += Decimal(serializer.data['costs'])
            event.save()
            return Response(status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        Event.objects.all().delete()
        return Response(status=status.HTTP_200_OK)