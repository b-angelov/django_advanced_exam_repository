from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from izpitnik.orth_calendar.models import Saint, HolidayOccurrences


class SaintsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Saint
        fields = '__all__'

class SaintsSerializerRelatedHolidays(SaintsSerializer):
    holiday_occurrences = serializers.StringRelatedField(
        many=True,
        source='occurrences'
    )

class SaintsSerializerRelatedFeasts(SaintsSerializer):
    related_feasts = serializers.StringRelatedField(
        many=True,
        source='feasts'
    )

class SaintsSerializerRelatedHolidaysAndFeasts(SaintsSerializerRelatedHolidays,SaintsSerializerRelatedFeasts):
    pass



