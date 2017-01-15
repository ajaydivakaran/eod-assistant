from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Team, Contributor, EndOfDayItem
from .permissions import StaffWritePermission, TeamEditOnly
from .serializers import TeamSerializer, \
    ContributorHyperlinkedRelationSerializer, ContributorPrimaryKeyRelationSerializer, \
    EndOfDayItemHyperlinkedRelationSerializer, EndOfDayItemPrimaryKeyRelationSerializer

GET_METHOD = 'GET'
HTML_CONTENT_TYPE = 'text/html'


class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffWritePermission, IsAuthenticated)
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Team.objects.all()
        return Team.objects.filter(user=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffWritePermission, IsAuthenticated)
    queryset = Contributor.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Contributor.objects.all()
        return Contributor.objects.filter(teams__user=self.request.user)

    def get_serializer_class(self):
        if self.request.content_type == HTML_CONTENT_TYPE or self.request.method == GET_METHOD:
            return ContributorHyperlinkedRelationSerializer
        return ContributorPrimaryKeyRelationSerializer


class EndOfDayItemViewSet(viewsets.ModelViewSet):
    permission_classes = (TeamEditOnly, IsAuthenticated)

    def get_queryset(self):
        if self.request.user.is_staff:
            return EndOfDayItem.objects.all()
        return EndOfDayItem.objects.filter(team__user=self.request.user)

    def get_serializer_class(self):
        if self.request.content_type == HTML_CONTENT_TYPE or self.request.method == GET_METHOD:
            return EndOfDayItemHyperlinkedRelationSerializer
        return EndOfDayItemPrimaryKeyRelationSerializer
