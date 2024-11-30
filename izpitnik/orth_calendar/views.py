from typing import Union

from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from izpitnik.orth_calendar.models import Saint, Feast
from izpitnik.orth_calendar.serializers.feasts import FeastsSerializer, FeastSerializerWithRelatedHolidays, \
    FeastSerializerWithRelatedSaints, FeastSerializerWithHolidaysAndSaints
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

class FeastListView(ListAPIView):
    queryset = Feast.objects.prefetch_related('occurrences','saint').all()

    def get_serializer_class(self):
        serializer = switch_serializer(
            get_v(self.request.GET.get('related_holidays')),
            get_v(self.request.GET.get('related_saints')),
            (FeastsSerializer,FeastSerializerWithRelatedHolidays,FeastSerializerWithRelatedSaints,FeastSerializerWithHolidaysAndSaints)

        )
        return serializer

class SingleFeastView(RetrieveAPIView):

    get_serializer_class = FeastListView.get_serializer_class
    queryset = Feast.objects.prefetch_related('occurrences','saint').all()




