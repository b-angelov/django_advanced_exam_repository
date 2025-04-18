from rest_framework import serializers

from izpitnik.articles.models import Article
from izpitnik.orth_calendar.models import Saint, Feast, HolidayOccurrences
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

    saint_ids = serializers.PrimaryKeyRelatedField(
        source='saint', many=True, write_only=True,
        queryset=Saint.objects.all(), required=False
    )
    feast_ids = serializers.PrimaryKeyRelatedField(
        source='feast', many=True, write_only=True,
        queryset=Feast.objects.all(), required=False
    )
    holiday_ids = serializers.PrimaryKeyRelatedField(
        source='holiday', many=True, write_only=True,
        queryset=HolidayOccurrences.objects.all(), required=False
    )

    image = serializers.ImageField(required=False,allow_null=True,allow_empty_file=True)



    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'image', 'saint', 'feast', 'holiday', 'author','saint_ids','feast_ids','holiday_ids','holiday_ids']
        read_only_fields = ['author']