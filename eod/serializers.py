from rest_framework import serializers

from .models import Team, Contributor, EndOfDayItem


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')


class ContributorHyperlinkedRelationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'first_name', 'last_name', 'display_name', 'is_active', 'team')


class ContributorPrimaryKeyRelationSerializer(ContributorHyperlinkedRelationSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())


class EndOfDayItemHyperlinkedRelationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EndOfDayItem
        fields = ('id', 'description', 'story_id', 'contributors', 'created_date')


class EndOfDayItemPrimaryKeyRelationSerializer(EndOfDayItemHyperlinkedRelationSerializer):
    contributors = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all())
