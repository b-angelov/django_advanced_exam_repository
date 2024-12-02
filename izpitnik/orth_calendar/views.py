from typing import Union

from django.shortcuts import render
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from requests import HTTPError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from izpitnik.orth_calendar.models import Saint, Feast, HolidayOccurrences
from izpitnik.orth_calendar.serializers.feasts import FeastsSerializer, FeastSerializerWithRelatedHolidays, \
    FeastSerializerWithRelatedSaints, FeastSerializerWithHolidaysAndSaints
from izpitnik.orth_calendar.serializers.holiday_occurrences import HolidayOccurrencesSerializer, HolidayByDateSerializer
from izpitnik.orth_calendar.serializers.saints import SaintsSerializer, SaintsSerializerRelatedHolidays, \
    SaintsSerializerRelatedFeasts, SaintsSerializerRelatedHolidaysAndFeasts



def switch_serializer(related_first, related_second, serializers:Union[list,tuple]):
    serializer = serializers[0]
    if related_first and not related_second:
        serializer = serializers[1]
    if related_second and not related_first:
        serializer = serializers[2]
    if related_second and related_first:
        serializer = serializers[3]
    return serializer


get_v = lambda x: {'true': True, '1': True}.get(x, False)



# Create your views here.
@extend_schema(
    request=SaintsSerializer,
    responses={201: SaintsSerializer, 400: SaintsSerializer},
    parameters=[
        OpenApiParameter(name='name', description='Saint name', type=str),
        OpenApiParameter(name='related_feasts', description='Load related feasts', type=str),
        OpenApiParameter(name='related_holidays', description='Load related holidays', type=str),
    ]
)
class SaintsListView(APIView):

    serializer_class = SaintsSerializer

    def get(self, request):
        name: str = request.GET.get('name')
        saints = Saint.objects.filter(name__icontains=name or '')
        serializer = switch_serializer(
            get_v(self.request.GET.get('related_holidays')),
            get_v(self.request.GET.get('related_feasts')),
        (SaintsSerializer,SaintsSerializerRelatedHolidays,SaintsSerializerRelatedFeasts,SaintsSerializerRelatedHolidaysAndFeasts)

        )
        serializer = serializer(saints, many=True)
        return Response(serializer.data)

@extend_schema(
    responses={201: SaintsSerializer, 400: SaintsSerializer},
    parameters=[
        OpenApiParameter(name='name', description='Saint name', type=str),
        OpenApiParameter(name='related_holidays', description='Load related holidays', type=str),
        OpenApiParameter(name='related_feasts', description='Load related feasts', type=str),

    ]
)
class SingleSaintView(RetrieveAPIView):
    queryset = Saint.objects.all()

    def get_serializer_class(self):
        serializer = switch_serializer(
            get_v(self.request.GET.get('related_holidays')),
            get_v(self.request.GET.get('related_feasts')),
        (SaintsSerializer,SaintsSerializerRelatedHolidays,SaintsSerializerRelatedFeasts,SaintsSerializerRelatedHolidaysAndFeasts)

        )
        return serializer


@extend_schema(
    responses={200: SaintsSerializer, 400: SaintsSerializer},
    parameters=[
        OpenApiParameter(name='name', description='Saint name', type=str),
        OpenApiParameter(name='related_holidays', description='Load related holidays', type=str),
        OpenApiParameter(name='related_saints', description='Load related saints', type=str),

    ]
)
class FeastListView(ListAPIView):
    queryset = Feast.objects.prefetch_related('occurrences','saint').all()

    def get_serializer_class(self):
        serializer = switch_serializer(
            get_v(self.request.GET.get('related_holidays')),
            get_v(self.request.GET.get('related_saints')),
            (FeastsSerializer,FeastSerializerWithRelatedHolidays,FeastSerializerWithRelatedSaints,FeastSerializerWithHolidaysAndSaints)

        )
        return serializer

@extend_schema(
    responses={200: SaintsSerializer, 400: SaintsSerializer},
    parameters=[
        OpenApiParameter(name='name', description='Saint name', type=str),
        OpenApiParameter(name='related_holidays', description='Load related holidays', type=str),
        OpenApiParameter(name='related_saints', description='Load related saints', type=str),

    ]
)
class SingleFeastView(RetrieveAPIView):

    get_serializer_class = FeastListView.get_serializer_class
    queryset = Feast.objects.prefetch_related('occurrences','saint').all()


class HolidayListView(ListAPIView):

    def get_queryset(self):
        queryset = HolidayOccurrences.objects.all()
        return queryset

    def get_serializer_class(self):
        return HolidayOccurrencesSerializer

@extend_schema(
    responses={200: SaintsSerializer, 400: SaintsSerializer},
    parameters=[
        OpenApiParameter(name='related', description='Load related feasts and saints on dates', type=str),
        OpenApiParameter(name='calendar', description='Switch calendars allowed types J G and JIG', type=str),

    ]
)
class SingleHolidayView(RetrieveAPIView):

    get_queryset = HolidayListView.get_queryset
    get_serializer_class = HolidayListView.get_serializer_class

@extend_schema(
    responses={200: SaintsSerializer, 400: SaintsSerializer},
    parameters=[
        OpenApiParameter(name='related', description='Load related feasts and saints on dates', type=str),
        OpenApiParameter(name='calendar', description='Switch calendars allowed types J G and JIG', type=str),

    ]
)
class SingleHolidayByDateView(RetrieveAPIView):

    # get_queryset = HolidayListView.get_queryset
    serializer_class = HolidayByDateSerializer
    lookup_url_kwarg = 'date_slug'

    # def get_object(self):
    #     return HolidayOccurrences(date=self.lookup_url_kwarg)

    def get_object(self):
        date = self.kwargs[self.lookup_url_kwarg]
        obj = HolidayOccurrences(date=date)
        calendar = self.request.GET.get('calendar')
        related_data = get_v(self.request.GET.get('related'))
        if calendar in obj.CalendarChoices._value2member_map_.keys():
            obj.calendar = calendar
        related_days = obj.get_distance()
        obj_data ={
            'date':obj.date,
            'easter_distance':related_days['easter'],
            'christmas_distance':related_days['christmas'],
            'calendar':obj.get_calendar_display,
            'feast':[],
            'saint':[],
        }
        if related_data:
            related_data = obj.saints_and_feasts_of_the_day()
            obj_data['feast'] = related_data['feasts']
            obj_data['saint'] = related_data['saints']

        return obj_data

    def get(self, *args, **kwargs):
        try:
            return super().get(*args,**kwargs)
        except (ValueError, AttributeError):
            return Response('Date not found or bad request!', status=status.HTTP_400_BAD_REQUEST)







