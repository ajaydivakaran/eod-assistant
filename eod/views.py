from rest_framework import viewsets

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
    permission_classes = (TeamEditOnly,)
    queryset = EndOfDayItem.objects.all()

    def get_serializer_class(self):
        if self.request.content_type == HTML_CONTENT_TYPE or self.request.method == GET_METHOD:
            return EndOfDayItemHyperlinkedRelationSerializer
        return EndOfDayItemPrimaryKeyRelationSerializer
