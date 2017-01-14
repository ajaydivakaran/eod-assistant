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
    permission_classes = (StaffWritePermission,)
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffWritePermission,)
    queryset = Contributor.objects.all()

    def get_serializer_class(self):
        if self.request.content_type == HTML_CONTENT_TYPE or self.request.method == GET_METHOD:
            return ContributorHyperlinkedRelationSerializer
        return ContributorPrimaryKeyRelationSerializer


class EndOfDayItemViewSet(viewsets.ModelViewSet):
    permission_classes = (TeamEditOnly, IsAuthenticated)
    queryset = EndOfDayItem.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return EndOfDayItem.objects.all()
        return EndOfDayItem.objects.filter(team__user=self.request.user)

    def get_serializer_class(self):
        if self.request.content_type == HTML_CONTENT_TYPE or self.request.method == GET_METHOD:
            return EndOfDayItemHyperlinkedRelationSerializer
        return EndOfDayItemPrimaryKeyRelationSerializer
