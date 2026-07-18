from fastapi import APIRouter, Depends, Path, Query, status

from app.coding_loop import service
from app.coding_loop.schemas import (
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectStatus,
    ProjectUpdate,
    RunCreate,
    RunListResponse,
    RunResponse,
    RunUpdate,
    TaskCreate,
    TaskListResponse,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
    TestErrorCreate,
    TestErrorListResponse,
    TestErrorResponse,
    TestErrorUpdate,
)
from app.notion.routes import _handle_notion_error, require_admin_key
from app.notion.schemas import DeleteResponse

router = APIRouter(
    prefix="/coding-loop",
    tags=["Autonomous Coding Loop"],
    dependencies=[Depends(require_admin_key)],
)


@router.get("/projects", response_model=ProjectListResponse)
def list_projects(
    project_status: ProjectStatus | None = Query(default=None, alias="status"),
    page_size: int = Query(default=50, ge=1, le=100),
    start_cursor: str | None = Query(default=None),
):
    try:
        return service.list_records(
            "projects", project_status, None, None, None, None, page_size, start_cursor
        )
    except Exception as error:
        _handle_notion_error(error)


@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(data: ProjectCreate):
    try:
        return service.create_record("projects", data)
    except Exception as error:
        _handle_notion_error(error)


@router.get("/projects/{page_id}", response_model=ProjectResponse)
def get_project(page_id: str = Path(min_length=1)):
    try:
        return service.get_record("projects", page_id)
    except Exception as error:
        _handle_notion_error(error)


@router.patch("/projects/{page_id}", response_model=ProjectResponse)
def update_project(data: ProjectUpdate, page_id: str = Path(min_length=1)):
    try:
        return service.update_record("projects", page_id, data)
    except Exception as error:
        _handle_notion_error(error)


@router.delete("/projects/{page_id}", response_model=DeleteResponse)
def delete_project(page_id: str = Path(min_length=1)):
    try:
        return service.delete_record(page_id)
    except Exception as error:
        _handle_notion_error(error)


@router.get("/tasks", response_model=TaskListResponse)
def list_tasks(
    task_status: TaskStatus | None = Query(default=None, alias="status"),
    project_id: str | None = Query(default=None),
    approved: bool | None = Query(default=None),
    page_size: int = Query(default=50, ge=1, le=100),
    start_cursor: str | None = Query(default=None),
):
    try:
        return service.list_records(
            "tasks",
            task_status,
            "Project",
            project_id,
            "Approved",
            approved,
            page_size,
            start_cursor,
        )
    except Exception as error:
        _handle_notion_error(error)


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(data: TaskCreate):
    try:
        return service.create_record("tasks", data)
    except Exception as error:
        _handle_notion_error(error)


@router.get("/tasks/{page_id}", response_model=TaskResponse)
def get_task(page_id: str = Path(min_length=1)):
    try:
        return service.get_record("tasks", page_id)
    except Exception as error:
        _handle_notion_error(error)


@router.patch("/tasks/{page_id}", response_model=TaskResponse)
def update_task(data: TaskUpdate, page_id: str = Path(min_length=1)):
    try:
        return service.update_record("tasks", page_id, data)
    except Exception as error:
        _handle_notion_error(error)


@router.delete("/tasks/{page_id}", response_model=DeleteResponse)
def delete_task(page_id: str = Path(min_length=1)):
    try:
        return service.delete_record(page_id)
    except Exception as error:
        _handle_notion_error(error)


@router.get("/runs", response_model=RunListResponse)
def list_runs(
    run_status: str | None = Query(default=None, alias="status"),
    task_id: str | None = Query(default=None),
    page_size: int = Query(default=50, ge=1, le=100),
    start_cursor: str | None = Query(default=None),
):
    try:
        return service.list_records(
            "runs", run_status, "Task", task_id, None, None, page_size, start_cursor
        )
    except Exception as error:
        _handle_notion_error(error)


@router.post(
    "/runs",
    response_model=RunResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_run(data: RunCreate):
    try:
        return service.create_record("runs", data)
    except Exception as error:
        _handle_notion_error(error)


@router.get("/runs/{page_id}", response_model=RunResponse)
def get_run(page_id: str = Path(min_length=1)):
    try:
        return service.get_record("runs", page_id)
    except Exception as error:
        _handle_notion_error(error)


@router.patch("/runs/{page_id}", response_model=RunResponse)
def update_run(data: RunUpdate, page_id: str = Path(min_length=1)):
    try:
        return service.update_record("runs", page_id, data)
    except Exception as error:
        _handle_notion_error(error)


@router.delete("/runs/{page_id}", response_model=DeleteResponse)
def delete_run(page_id: str = Path(min_length=1)):
    try:
        return service.delete_record(page_id)
    except Exception as error:
        _handle_notion_error(error)


@router.get("/test-errors", response_model=TestErrorListResponse)
def list_test_errors(
    error_status: str | None = Query(default=None, alias="status"),
    page_size: int = Query(default=50, ge=1, le=100),
    start_cursor: str | None = Query(default=None),
):
    try:
        return service.list_records(
            "test-errors", error_status, None, None, None, None, page_size, start_cursor
        )
    except Exception as error:
        _handle_notion_error(error)


@router.post(
    "/test-errors",
    response_model=TestErrorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_test_error(data: TestErrorCreate):
    try:
        return service.create_record("test-errors", data)
    except Exception as error:
        _handle_notion_error(error)


@router.get("/test-errors/{page_id}", response_model=TestErrorResponse)
def get_test_error(page_id: str = Path(min_length=1)):
    try:
        return service.get_record("test-errors", page_id)
    except Exception as error:
        _handle_notion_error(error)


@router.patch("/test-errors/{page_id}", response_model=TestErrorResponse)
def update_test_error(data: TestErrorUpdate, page_id: str = Path(min_length=1)):
    try:
        return service.update_record("test-errors", page_id, data)
    except Exception as error:
        _handle_notion_error(error)


@router.delete("/test-errors/{page_id}", response_model=DeleteResponse)
def delete_test_error(page_id: str = Path(min_length=1)):
    try:
        return service.delete_record(page_id)
    except Exception as error:
        _handle_notion_error(error)
