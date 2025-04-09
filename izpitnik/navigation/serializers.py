from rest_framework import serializers

from izpitnik.navigation.models import Navigation

class NavigationSerializer(serializers.ModelSerializer):

    menu = serializers.StringRelatedField(
        many=True,
        source='menu.all'
    )

    language = serializers.StringRelatedField(
        many=True,
        source="language.all"
    )

    children = serializers.SerializerMethodField(
        method_name='get_children'
    )

    def get_children(self, obj):
        return NavigationSerializer(
            obj.children.all(),
            many=True,
            read_only=True
        ).data

    class Meta:
        model = Navigation
        exclude = ['id']

class MenuSerializer(serializers.ModelSerializer):

    items = NavigationSerializer(
        many=True,
        read_only=True
    )

    parent_id = NavigationSerializer(
        many=True,
        read_only=True,
        source="children"
    )

    class Meta:
        model = Navigation
        exclude = ['id']

