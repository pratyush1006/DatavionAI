"""
Resolve normalized reverse-geocoding data against canonical Geography references.
"""

from __future__ import annotations

from apps.platform.geography.models import AdministrativeRegion, City, Country


def resolve_reference_entities(
    *, country_code: str = "", state: str = "", city: str = ""
) -> dict:
    """Return best-effort canonical reference IDs without creating data."""
    result = {
        "country_id": None,
        "region_id": None,
        "city_id": None,
        "timezone": "",
    }

    code = (country_code or "").strip().upper()
    if code:
        country = Country.objects.filter(code=code).first()
        if country is not None:
            result["country_id"] = str(country.pk)
            if state:
                region = AdministrativeRegion.objects.filter(
                    country=country, name__iexact=state.strip()
                ).first()
                if region is not None:
                    result["region_id"] = str(region.pk)
                    if city:
                        city_obj = City.objects.filter(
                            country=country, region=region, name__iexact=city.strip()
                        ).first()
                        if city_obj is not None:
                            result["city_id"] = str(city_obj.pk)
                            result["timezone"] = city_obj.timezone
                    return result

            if city:
                city_obj = City.objects.filter(
                    country=country, name__iexact=city.strip()
                ).first()
                if city_obj is not None:
                    result["city_id"] = str(city_obj.pk)
                    result["timezone"] = city_obj.timezone
    return result


__all__ = ("resolve_reference_entities",)
