import mimesis
import mimesis.exceptions
from beanie import PydanticObjectId
from beanie.odm.operators.find.geospatial import Near
from demo_app.models import Address, GeoJson2DPoint, Paged
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

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


@address_router.get("/{id}/", response_model=Address)
async def get_location(id: PydanticObjectId) -> Address:
    address = await Address.get(document_id=id)
    if not address:
        raise HTTPException(status_code=404)
    return address


@address_router.get("/{id}/nearby")
async def get_nearby_locations(
    id: PydanticObjectId, page_size: int = 100, page_start: int = 0
) -> Paged[Address]:
    address = await Address.get(document_id=id)
    if not address:
        raise HTTPException(status_code=404)
    query = Address.find(
        Near(
            Address.geo,
            longitude=address.geo.coordinates[0],
            latitude=address.geo.coordinates[1],
        )
    )
    number = await query.count()
    results = await query.limit(page_size).skip(page_start).to_list()
    return Paged(
        number,
        results,
        page_size + page_start < number,
    )


@address_router.post("/seed")
async def seed_addresses(count: int = 1000, locale: str = "en"):
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
                    geo=GeoJson2DPoint(
                        coordinates=(address.longitude(), address.latitude())
                    ),
                    postal_code=address.postal_code(),
                )
            )
    except mimesis.exceptions.UnsupportedLocale:
        return {"message": f"Locale {locale} not supported"}
    await Address.insert_many(data)
    return {"message": f"Created {count} addresses"}
