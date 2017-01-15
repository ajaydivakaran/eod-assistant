from rest_framework import serializers

from .models import Contributor, Team


class ContributorsPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        super(ContributorsPrimaryKeyRelatedField, self).__init__(**kwargs)

    def get_queryset(self):
        request = self.context['request']
        if request.user.is_staff:
            return Contributor.objects.all()
        return Contributor.objects.filter(teams__user=request.user)


class TeamsPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        super(TeamsPrimaryKeyRelatedField, self).__init__(**kwargs)

    def get_queryset(self):
        request = self.context['request']
        if request.user.is_staff:
            return Team.objects.all()
        return Team.objects.filter(user=request.user)
