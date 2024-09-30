import typing as t

from anyio.abc import value
from psycopg import AsyncConnection

from . import domain as d
from .domain import Commitment


class InvestorsStore(t.Protocol):
    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    async def get_investors(
        self, *, offset: int, limit: int
    ) -> t.Sequence[d.Investor]: ...

    async def asset_classes(self, investor_id: int) -> t.Iterable[d.AssetClass]: ...

    async def commitments(
        self, investor_id: int, *, asset_class_id: int | None, offset: int, limit: int
    ) -> t.Sequence[d.Commitment]: ...


GET_INVESTORS_QUERY = """
with investor_commitments as (
    select investor_id, sum(amount) as total_commitment
    from commitment group by investor_id
)
select investor.id,
       investor.name,
       investory_type.name as investory_type_name,
       investor.date_added,
       country.name        as country_name,
       investor_commitments.total_commitment
from investor
         join investor_commitments on investor.id = investor_commitments.investor_id
         join investory_type on investor.type_id = investory_type.id
         join country on investor.country_id = country.id
order by investor.id
offset %s
limit %s;
"""

ASSET_CLASSES_QUERY = """select class_id, asset_class.name, sum(amount)
from commitment
         join asset_class on commitment.class_id = asset_class.id
where investor_id = %s
group by class_id, asset_class.name
order by asset_class.name"""


GET_COMMITMENTS_QUERY = """
select commitment.id, asset_class.name, currency_symbol as currency, amount
from commitment
         join asset_class on commitment.class_id = asset_class.id
where investor_id = %s
order by commitment.id
offset %s
limit %s;
"""

GET_COMMITMENTS_QUERY_FILTER_ASSET_CLASS = """
select commitment.id, asset_class.name, currency_symbol as currency, amount
from commitment
         join asset_class on commitment.class_id = asset_class.id
where investor_id = %s and commitment.class_id = %s
order by commitment.id
offset %s
limit %s;
"""


class PostgresqlStore(InvestorsStore):
    def __init__(self, db_url: str):
        self._db_url = db_url
        self._connection = None

    async def __aenter__(self):
        if self._connection:
            raise RuntimeError("already connected")

        self._connection = await AsyncConnection.connect(self._db_url)
        await self._connection.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._connection.__aexit__(exc_type, exc_val, exc_tb)
        self._connection = None

    async def get_investors(self, *, offset: int, limit: int) -> t.Sequence[d.Investor]:
        if not self._connection:
            raise RuntimeError("store should be used as async context manager")
        async with self._connection.cursor() as cursor:
            result = await cursor.execute(GET_INVESTORS_QUERY, (offset, limit))
            return [
                d.Investor(
                    id=id_,
                    name=name,
                    type=type_,
                    date_added=date_added,
                    address=address,
                    total_commitment=int(total_commitment),
                )
                for (
                    id_,
                    name,
                    type_,
                    date_added,
                    address,
                    total_commitment,
                ) in await result.fetchall()
            ]

    async def asset_classes(self, investor_id: int) -> t.Iterable[d.AssetClass]:
        if not self._connection:
            raise RuntimeError("store should be used as async context manager")
        async with self._connection.cursor() as cursor:
            result = await cursor.execute(ASSET_CLASSES_QUERY, (investor_id,))
            return [
                d.AssetClass(id=id, name=name, value=int(value)) for (id, name, value) in await result.fetchall()
            ]


    async def commitments(
        self,
        investor_id: int,
        *,
        asset_class_id: int | None = None,
        offset: int,
        limit: int,
    ) -> t.Sequence[d.Commitment]:
        if not self._connection:
            raise RuntimeError("store should be used as async context manager")
        async with self._connection.cursor() as cursor:
            if asset_class_id is not None:
                result = await cursor.execute(
                    GET_COMMITMENTS_QUERY_FILTER_ASSET_CLASS,
                    (investor_id, asset_class_id, offset, limit),
                )
            else:
                result = await cursor.execute(
                    GET_COMMITMENTS_QUERY, (investor_id, offset, limit)
                )
            return [
                Commitment(
                    id=id, asset_class=asset_class, currency=currency, amount=amount
                )
                for (id, asset_class, currency, amount) in await result.fetchall()
            ]


def get_investors_store(db_url: str) -> InvestorsStore:
    if not db_url.startswith("postgresql"):
        raise RuntimeError("only postgresql store is supported")
    return PostgresqlStore(db_url)
