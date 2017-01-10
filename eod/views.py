from rest_framework import viewsets

from .models import Team, Contributor
from .serializers import TeamSerializer, ContributorHtmlSerializer, ContributorNonHtmlSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()

    def get_serializer_class(self):
        if self.request.content_type == 'text/html':
            return ContributorHtmlSerializer
        return ContributorNonHtmlSerializer
