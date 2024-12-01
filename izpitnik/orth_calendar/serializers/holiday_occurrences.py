from rest_framework import serializers

from izpitnik.orth_calendar.models import HolidayOccurrences
from izpitnik.orth_calendar.serializers.feasts import FeastsSerializer
from izpitnik.orth_calendar.serializers.saints import SaintsSerializer


class HolidayOccurrencesSerializer(serializers.ModelSerializer):


    calendar = serializers.StringRelatedField(
        source = 'get_calendar_display'
    )

    class Meta:
        model = HolidayOccurrences
        exclude = ['feast', 'saint', 'date']

class HolidayByDateSerializer(serializers.ModelSerializer):

    feast = FeastsSerializer(
        many=True,
        read_only=True
    )
    saint = SaintsSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = HolidayOccurrences
        exclude = ['id']