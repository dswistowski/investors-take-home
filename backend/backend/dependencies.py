import os
import typing as t

from fastapi import Depends

from backend.investors_store import get_investors_store


def database_url() -> str:
    return os.environ["DB_URL"]


async def investors_store(database_url: t.Annotated[str, Depends(database_url)]):
    store = get_investors_store(database_url)
    async with store:
        yield store
