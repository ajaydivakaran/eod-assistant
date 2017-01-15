from rest_framework import serializers

from .models import Team, Contributor, EndOfDayItem
from .relations import ContributorsPrimaryKeyRelatedField, TeamsPrimaryKeyRelatedField


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')


class ContributorHyperlinkedRelationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'first_name', 'last_name', 'display_name', 'is_active', 'teams')


class ContributorPrimaryKeyRelationSerializer(ContributorHyperlinkedRelationSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())


class EndOfDayItemHyperlinkedRelationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EndOfDayItem
        fields = ('id', 'story_id', 'description', 'status', 'contributors', 'created_date', 'team')


class EndOfDayItemPrimaryKeyRelationSerializer(EndOfDayItemHyperlinkedRelationSerializer):
    contributors = ContributorsPrimaryKeyRelatedField(many=True)
    team = TeamsPrimaryKeyRelatedField()
