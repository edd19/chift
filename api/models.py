from django.db import models
from django.utils.translation import gettext_lazy as _


class Partner(models.Model):
    partner_id = models.IntegerField(unique=True, help_text=_("Id of the partner"))

    name = models.CharField(max_length=120, help_text=_("Name"))
    email = models.EmailField(max_length=256, help_text=_("Email"))

    country_code = models.CharField(max_length=3, help_text=_("The ISO country code in two chars."))

    employee = models.BooleanField(help_text=_("Check this box if this contact is an Employee."))
    is_company = models.BooleanField(help_text=_("Check if the contact is a company, otherwise it is a person"))

    def __str__(self) -> str:
        return f"{self.name} ({self.country_code})"
