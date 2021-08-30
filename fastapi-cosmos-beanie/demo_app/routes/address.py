from typing import Optional

import mimesis
import mimesis.exceptions
from demo_app.models import Address, Paged
from fastapi import APIRouter

address_router = APIRouter()


@address_router.get("/")
async def list_addresses(page_size: int = 100, page_start: int = 0) -> Paged[Address]:
    number = await Address.count()
    return Paged(
        number,
        await Address.all(limit=page_size, skip=page_start)
        .sort(Address.postal_code)
        .to_list(),
        page_size + page_start < number,
    )


@address_router.get("/find")
async def find_addresses(
    country: str, page_size: int = 100, page_start: int = 0
) -> Paged[Address]:
    query = Address.find(Address.country == country)
    number = await query.count()
    results = (
        await query.limit(page_size)
        .skip(page_start)
        .sort(Address.postal_code)
        .to_list()
    )
    return Paged(
        number,
        results,
        page_size + page_start < number,
    )


@address_router.post("/seed")
async def seed_addresses(count: int = 1000, locale: str = "en-us"):
    """
    Fill the addresses collection with dummy data.
    """
    data = []
    try:
        for _ in range(count):
            address = mimesis.Address(locale=locale)

            data.append(
                Address(
                    street_number=address.street_number(),
                    street_name=address.street_name(),
                    city=address.city(),
                    country=address.country(),
                    longitude=address.longitude(),
                    latitude=address.latitude(),
                    postal_code=address.postal_code(),
                )
            )
    except mimesis.exceptions.UnsupportedLocale:
        return {"message": f"Locale {locale} not supported"}
    await Address.insert_many(data)
    return {"message": f"Created {count} addresses"}
