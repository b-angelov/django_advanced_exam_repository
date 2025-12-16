from rest_framework import serializers

# from izpitnik.accounts.models import User
from izpitnik.accounts.serializers import UserBasicSerializer
from izpitnik.articles.models import Article, Likes
from izpitnik.orth_calendar.models import Saint, Feast, HolidayOccurrences
from izpitnik.orth_calendar.serializers.feasts import FeastsSerializer
from izpitnik.orth_calendar.serializers.holiday_occurrences import HolidayOccurrencesSerializer
from izpitnik.orth_calendar.serializers.saints import SaintsSerializer

class LikesSerializer(serializers.Serializer):

    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()


    def get_likes_count(self, obj):
        article = self.context.get('article', None)
        print(self.context)
        return Likes.objects.filter(article=article).count()


    def get_liked_by_user(self, obj):
        user = self.context.get('user', None)
        if not user.is_authenticated:
            return False
        article = self.context.get('article',None)
        return Likes.objects.filter(article=article, user=user).exists()

    class Meta:
        fields = ['likes_count', 'liked_by_user']
        exclude = []

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
    author = UserBasicSerializer(
        read_only=True,
        many=False,
    )

    image = serializers.ImageField(required=False,allow_null=True,allow_empty_file=True)

    likes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return LikesSerializer({}, context={"article":obj,"user":self.context.get('request').user}).data



    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'image', 'saint', 'feast', 'holiday', 'author','saint_ids','feast_ids','holiday_ids','holiday_ids', 'likes']
        read_only_fields = ['author']