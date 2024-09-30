import typing as t

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from . import dependencies as dep
from . import domain as d
from . import response as r
from .investors_store import InvestorsStore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEFAULT_PAGINATION_LIMIT = 1_000


@app.get("/investors/")
async def investors(
    investors_store: t.Annotated[InvestorsStore, Depends(dep.investors_store)],
    offset: t.Annotated[int, Query(ge=0)] = 0,
    limit: t.Annotated[int, Query()] = DEFAULT_PAGINATION_LIMIT,
) -> r.PaginatedResponse[d.Investor]:
    data = await investors_store.get_investors(offset=offset, limit=limit + 1)
    next_, previous = None, None
    if len(data) > limit:
        next_ = f"/investors/?offset={offset + limit}&limit={limit}"
    if offset > 0:
        previous = f"/investors/?offset={max(0, offset - limit)}&limit={limit}"
    return r.PaginatedResponse(
        data=data[:limit], paging=r.Pagination(next=next_, previous=previous)
    )


@app.get("/investors/{investor_id}/asset-classes/")
async def asset_classes(
    investors_store: t.Annotated[InvestorsStore, Depends(dep.investors_store)],
    investor_id: int,
) -> t.Iterable[d.AssetClass]:
    return await investors_store.asset_classes(investor_id=investor_id)


@app.get("/investors/{investor_id}/commitment/")
async def commitments(
    investors_store: t.Annotated[InvestorsStore, Depends(dep.investors_store)],
    investor_id: int,
    asset_class_id: t.Annotated[int | None, Query()] = None,
    offset: t.Annotated[int, Query(ge=0)] = 0,
    limit: t.Annotated[int, Query()] = DEFAULT_PAGINATION_LIMIT,
) -> r.PaginatedResponse[d.Commitment]:
    data = await investors_store.commitments(
        investor_id, asset_class_id=asset_class_id, offset=offset, limit=limit + 1
    )

    next_, previous = None, None
    if len(data) > limit:
        next_ = (
            f"/investors/{investor_id}/commitment/"
            f"?offset={offset + limit}&limit={limit}"
        )
    if offset > 0:
        previous = (
            f"/investors/{investor_id}/commitment/"
            f"?offset={max(0, offset - limit)}&limit={limit}"
        )
    return r.PaginatedResponse(
        data=data[:limit], paging=r.Pagination(next=next_, previous=previous)
    )


@app.get("/health/")
def health() -> t.Literal["OK"]:
    return "OK"
