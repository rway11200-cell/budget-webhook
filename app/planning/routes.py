from fastapi import APIRouter, Depends, Path, Query, status

from app.notion.routes import _handle_notion_error, require_admin_key
from app.planning import service
from app.planning.schemas import (
    Month,
    PlanningItemCreate,
    PlanningItemListResponse,
    PlanningItemResponse,
    PlanningItemUpdate,
    PlanningSummaryResponse,
)
from app.notion.schemas import DeleteResponse

router = APIRouter(
    prefix="/planning",
    tags=["Planning 2026"],
    dependencies=[Depends(require_admin_key)],
)


@router.get("/items", response_model=PlanningItemListResponse)
def list_items(
    year: str | None = Query(default=None),
    month: Month | None = Query(default=None),
    tag: str | None = Query(default=None),
    completed: bool | None = Query(default=None),
    page_size: int = Query(default=50, ge=1, le=100),
    start_cursor: str | None = Query(default=None),
):
    try:
        return service.list_items(year, month, tag, completed, page_size, start_cursor)
    except Exception as error:
        _handle_notion_error(error)


@router.post(
    "/items",
    response_model=PlanningItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(data: PlanningItemCreate):
    try:
        return service.create_item(data)
    except Exception as error:
        _handle_notion_error(error)


@router.get("/items/{page_id}", response_model=PlanningItemResponse)
def get_item(page_id: str = Path(min_length=1)):
    try:
        return service.get_item(page_id)
    except Exception as error:
        _handle_notion_error(error)


@router.patch("/items/{page_id}", response_model=PlanningItemResponse)
def update_item(data: PlanningItemUpdate, page_id: str = Path(min_length=1)):
    try:
        return service.update_item(page_id, data)
    except Exception as error:
        _handle_notion_error(error)


@router.delete("/items/{page_id}", response_model=DeleteResponse)
def delete_item(page_id: str = Path(min_length=1)):
    try:
        return service.delete_item(page_id)
    except Exception as error:
        _handle_notion_error(error)


@router.get("/pending", response_model=list[PlanningItemResponse])
def pending_items(
    year: str | None = Query(default="2026"),
    month: Month | None = Query(default=None),
    tag: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
):
    try:
        return service.pending_items(year, month, tag, limit)
    except Exception as error:
        _handle_notion_error(error)


@router.get("/summary", response_model=PlanningSummaryResponse)
def summary(
    year: str | None = Query(default="2026"),
    month: Month | None = Query(default=None),
    tag: str | None = Query(default=None),
):
    try:
        return service.get_summary(year, month, tag)
    except Exception as error:
        _handle_notion_error(error)
