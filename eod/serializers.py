from rest_framework import serializers

from .models import Team, Contributor


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')


class ContributorHtmlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id', 'first_name', 'last_name', 'display_name', 'is_active', 'team')


class ContributorNonHtmlSerializer(ContributorHtmlSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
