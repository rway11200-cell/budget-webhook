from app.config import (
    CODING_LOOP_ERRORS_DATABASE_ID,
    CODING_LOOP_PROJECTS_DATABASE_ID,
    CODING_LOOP_RUNS_DATABASE_ID,
    CODING_LOOP_TASKS_DATABASE_ID,
)
from app.notion import repository as notion_repository

DATABASES = {
    "projects": CODING_LOOP_PROJECTS_DATABASE_ID,
    "tasks": CODING_LOOP_TASKS_DATABASE_ID,
    "runs": CODING_LOOP_RUNS_DATABASE_ID,
    "test-errors": CODING_LOOP_ERRORS_DATABASE_ID,
}


def query(resource: str, payload: dict) -> dict:
    return notion_repository.query_database(DATABASES[resource], payload)


def create(resource: str, properties: dict) -> dict:
    return notion_repository.create_page(
        DATABASES[resource],
        {"properties": properties},
    )


def get(page_id: str) -> dict:
    return notion_repository.get_page(page_id)


def update(page_id: str, properties: dict) -> dict:
    return notion_repository.update_page(page_id, {"properties": properties})


def archive(page_id: str) -> dict:
    return notion_repository.archive_page(page_id)
