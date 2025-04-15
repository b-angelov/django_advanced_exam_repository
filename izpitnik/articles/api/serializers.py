from rest_framework import serializers

from izpitnik.articles.models import Article
from izpitnik.orth_calendar.serializers.feasts import FeastsSerializer
from izpitnik.orth_calendar.serializers.holiday_occurrences import HolidayOccurrencesSerializer
from izpitnik.orth_calendar.serializers.saints import SaintsSerializer


class ArticleSerializer(serializers.ModelSerializer):

    saint = SaintsSerializer(
        many=True,
        read_only=True
    )

    feast = FeastsSerializer(
        many=True,
        read_only=True
    )

    holiday = HolidayOccurrencesSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'image', 'saint', 'feast', 'holiday', 'author']
        read_only_fields = ['author']