from rest_framework import serializers
from rest_framework.generics import ListAPIView

from izpitnik.orth_calendar.models import Feast
from izpitnik.orth_calendar.serializers.saints import SaintsSerializer


class FeastsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feast
        exclude = ['saint']

class FeastSerializerWithRelatedSaints(FeastsSerializer):

    related_saints = SaintsSerializer(many=True,read_only=True,source='saint')


class FeastSerializerWithRelatedHolidays(FeastsSerializer):

    related_holidays = serializers.PrimaryKeyRelatedField(
        many=True,
        source='occurrences',
        read_only=True
    )


class FeastSerializerWithHolidaysAndSaints(FeastSerializerWithRelatedSaints,FeastSerializerWithRelatedHolidays):
    pass