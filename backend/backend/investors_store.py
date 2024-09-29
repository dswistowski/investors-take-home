import typing as t

from psycopg import AsyncConnection

from . import domain as d


class InvestorsStore(t.Protocol):
    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    async def get_investors(
        self, offset: int, limit: int
    ) -> t.Sequence[d.Investor]: ...


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

    async def get_investors(self, offset: int, limit: int) -> t.Sequence[d.Investor]:
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


def get_investors_store(db_url: str) -> InvestorsStore:
    if not db_url.startswith("postgresql"):
        raise RuntimeError("only postgresql store is supported")
    return PostgresqlStore(db_url)
