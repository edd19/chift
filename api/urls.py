from django.urls import path

from api.views import PartnersListView, PartnerDetailView

app_name = "api"
urlpatterns = [
    path("partner/<int:pk>", PartnerDetailView.as_view(), name="partner-detail"),
    path("partners/", PartnersListView.as_view(), name="partner-list"),
]
