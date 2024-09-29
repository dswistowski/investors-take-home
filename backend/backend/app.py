import typing as t

from fastapi import Depends, FastAPI, Query

from . import dependencies as dep
from . import domain as d
from . import response as r
from .investors_store import InvestorsStore

app = FastAPI()
DEFAULT_PAGINATION_LIMIT = 1_000


@app.get("/investors/")
async def investors(
    investors_store: t.Annotated[InvestorsStore, Depends(dep.investors_store)],
    offset: t.Annotated[int, Query(ge=0)] = 0,
    limit: t.Annotated[int, Query()] = DEFAULT_PAGINATION_LIMIT,
) -> r.PaginatedResponse[d.Investor]:
    data = await investors_store.get_investors(offset, limit + 1)
    next_, previous = None, None
    if len(data) > limit:
        next_ = f"/investors/?offset={offset + limit}&limit={limit}"
    if offset > 0:
        previous = f"/investors/?offset={max(0, offset - limit)}&limit={limit}"
    return r.PaginatedResponse(
        data=data[:limit], paging=r.Pagination(next=next_, previous=previous)
    )


@app.get("/health/")
def health() -> t.Literal["OK"]:
    return "OK"
