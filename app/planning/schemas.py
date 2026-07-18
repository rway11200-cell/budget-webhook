from typing import Literal

from pydantic import BaseModel, Field

Month = Literal[
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


class PlanningItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    year: str | None = Field(default="2026", max_length=20)
    month: Month | None = None
    tags: list[str] = Field(default_factory=list)
    estimated_budget: float | None = Field(default=None, ge=0)
    completed: bool = False


class PlanningItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    year: str | None = Field(default=None, max_length=20)
    month: Month | None = None
    tags: list[str] | None = None
    estimated_budget: float | None = Field(default=None, ge=0)
    completed: bool | None = None


class PlanningItemResponse(BaseModel):
    id: str
    name: str
    year: str | None = None
    month: str | None = None
    tags: list[str]
    estimated_budget: float | None = None
    completed: bool
    url: str | None = None
    created_time: str | None = None
    last_edited_time: str | None = None


class PlanningItemListResponse(BaseModel):
    items: list[PlanningItemResponse]
    next_cursor: str | None = None
    has_more: bool = False


class PlanningGroupSummary(BaseModel):
    name: str
    item_count: int
    completed_count: int
    estimated_budget: float


class PlanningSummaryResponse(BaseModel):
    item_count: int
    completed_count: int
    pending_count: int
    estimated_budget: float
    completed_budget: float
    pending_budget: float
    by_month: list[PlanningGroupSummary]
    by_tag: list[PlanningGroupSummary]
