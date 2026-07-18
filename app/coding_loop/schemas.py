from typing import Literal

from pydantic import BaseModel, Field

Priority = Literal["Low", "Medium", "High"]
ProjectStatus = Literal["Active", "Paused", "Archived"]
TaskStatus = Literal["To-do", "Ready", "In Progress", "Needs review", "Done", "Blocked"]


class NotionRecord(BaseModel):
    id: str
    url: str | None = None
    created_time: str | None = None
    last_edited_time: str | None = None


class ProjectCreate(BaseModel):
    project: str = Field(min_length=1, max_length=200)
    auto_commit: bool = False
    branch: str | None = None
    opencode_session: str | None = None
    priority: Priority | None = None
    repo_path: str | None = None
    status: ProjectStatus = "Active"
    updated: str | None = None


class ProjectUpdate(BaseModel):
    project: str | None = Field(default=None, min_length=1, max_length=200)
    auto_commit: bool | None = None
    branch: str | None = None
    opencode_session: str | None = None
    priority: Priority | None = None
    repo_path: str | None = None
    status: ProjectStatus | None = None
    updated: str | None = None


class ProjectResponse(NotionRecord):
    project: str
    auto_commit: bool
    branch: str | None = None
    opencode_session: str | None = None
    priority: Priority | None = None
    repo_path: str | None = None
    status: ProjectStatus
    updated: str | None = None


class TaskCreate(BaseModel):
    task: str = Field(min_length=1, max_length=200)
    approved: bool = False
    attempts: float | None = Field(default=0, ge=0)
    created: str | None = None
    last_result: str | None = None
    next_actions: str | None = None
    priority: Priority | None = None
    project_id: str | None = None
    status: TaskStatus = "To-do"
    updated: str | None = None


class TaskUpdate(BaseModel):
    task: str | None = Field(default=None, min_length=1, max_length=200)
    approved: bool | None = None
    attempts: float | None = Field(default=None, ge=0)
    created: str | None = None
    last_result: str | None = None
    next_actions: str | None = None
    priority: Priority | None = None
    project_id: str | None = None
    status: TaskStatus | None = None
    updated: str | None = None


class TaskResponse(NotionRecord):
    task: str
    approved: bool
    attempts: float | None = None
    created: str | None = None
    last_result: str | None = None
    next_actions: str | None = None
    priority: Priority | None = None
    project_id: str | None = None
    status: TaskStatus
    updated: str | None = None


class RunCreate(BaseModel):
    run_id: str = Field(min_length=1, max_length=200)
    duration: float | None = Field(default=None, ge=0)
    openai_available: bool = False
    status: str | None = None
    summary: str | None = None
    task_id: str | None = None
    timestamp: str | None = None


class RunUpdate(BaseModel):
    run_id: str | None = Field(default=None, min_length=1, max_length=200)
    duration: float | None = Field(default=None, ge=0)
    openai_available: bool | None = None
    status: str | None = None
    summary: str | None = None
    task_id: str | None = None
    timestamp: str | None = None


class RunResponse(NotionRecord):
    run_id: str
    duration: float | None = None
    openai_available: bool
    status: str | None = None
    summary: str | None = None
    task_id: str | None = None
    timestamp: str | None = None


class TestErrorCreate(BaseModel):
    run_id: str = Field(min_length=1, max_length=200)
    duration: float | None = Field(default=None, ge=0)
    status: str | None = None
    summary: str | None = None
    timestamp: str | None = None


class TestErrorUpdate(BaseModel):
    run_id: str | None = Field(default=None, min_length=1, max_length=200)
    duration: float | None = Field(default=None, ge=0)
    status: str | None = None
    summary: str | None = None
    timestamp: str | None = None


class TestErrorResponse(NotionRecord):
    run_id: str
    duration: float | None = None
    status: str | None = None
    summary: str | None = None
    timestamp: str | None = None


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    next_cursor: str | None = None
    has_more: bool = False


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    next_cursor: str | None = None
    has_more: bool = False


class RunListResponse(BaseModel):
    items: list[RunResponse]
    next_cursor: str | None = None
    has_more: bool = False


class TestErrorListResponse(BaseModel):
    items: list[TestErrorResponse]
    next_cursor: str | None = None
    has_more: bool = False
