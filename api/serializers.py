from rest_framework import serializers

from api.models import Partner


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ["name", "email", "country_code", "employee", "is_company"]
