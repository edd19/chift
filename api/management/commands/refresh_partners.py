import xmlrpc.client
from typing import List, Dict, Tuple

from django.conf import settings
from django.core.management.base import BaseCommand
from api.models import Partner


class Command(BaseCommand):
    help = "Refresh Partner database"

    def handle(self, *args, **options):
        self.stdout.write("Fetching odoo partners ....")
        odoo_partners = fetch_odoo_partners()
        self.stdout.write(f"{len(odoo_partners)} odoo partners fetched !!")

        self.stdout.write(f"Upserting odoo partners into Partner database ...")
        for odoo_partner in odoo_partners:
            upsert_odoo_partner(odoo_partner)

        self.stdout.write(f"Removing partners from dabatase ...")
        partners_removed = remove_partners(odoo_partners)
        self.stdout.write(f"{len(partners_removed)} partners removed !!")

        self.stdout.write(
            self.style.SUCCESS("Successfully refreshed partners")
        )


def fetch_odoo_partners() -> List[Dict]:
    odoo_settings = settings.ODOO_SETTINGS
    url = odoo_settings["url"]
    db = odoo_settings["db"]
    username = odoo_settings["username"]
    password = odoo_settings["password"]

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})

    odoo_models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return odoo_models.execute_kw(
        db,
        uid,
        password,
        'res.partner',
        'search_read',
        [[]],
        {"fields": ["id", "name", "email", "country_code", "employee", "is_company"]}
    )


def upsert_odoo_partner(odoo_partner: Dict) -> Tuple['Partner', bool]:
    return Partner.objects.update_or_create(
        partner_id=odoo_partner['id'],
        defaults={
            "name": _clean_odoo_value(odoo_partner["name"], "UNDEFINED"),
            "email": _clean_odoo_value(odoo_partner["email"], ""),
            "country_code": _clean_odoo_value(odoo_partner["country_code"], ""),
            "employee": odoo_partner["employee"],
            "is_company": odoo_partner["is_company"],
        }
    )


def _clean_odoo_value(odoo_value, default_value):
    if odoo_value is False:
        return default_value
    return odoo_value


def remove_partners(odoo_partners: List[Dict]) -> List['Partner']:
    odoo_partners_id = [odoo_partner['id'] for odoo_partner in odoo_partners]
    partners_to_remove = Partner.objects.exclude(partner_id__in=odoo_partners_id)

    for partner in partners_to_remove:
        partner.delete()

    return partners_to_remove

