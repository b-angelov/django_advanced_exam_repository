from rest_framework import serializers

from izpitnik.orth_calendar.models import HolidayOccurrences


class HolidayOccurrencesSerializer(serializers.ModelSerializer):

    calendar = serializers.StringRelatedField(
        source = 'get_calendar_display'
    )

    class Meta:
        model = HolidayOccurrences
        exclude = ['feast', 'saint']