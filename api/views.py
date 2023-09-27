from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Partner
from api.serializers import PartnerSerializer


class PartnersListView(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PartnerDetailView(RetrieveAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = "pk"
