from app.config import PLANNING_2026_DATABASE_ID
from app.notion import repository as notion_repository


def query_items(payload: dict) -> dict:
    return notion_repository.query_database(PLANNING_2026_DATABASE_ID, payload)


def create_item(properties: dict) -> dict:
    return notion_repository.create_page(
        PLANNING_2026_DATABASE_ID,
        {"properties": properties},
    )


def get_item(page_id: str) -> dict:
    return notion_repository.get_page(page_id)


def update_item(page_id: str, properties: dict) -> dict:
    return notion_repository.update_page(page_id, {"properties": properties})


def archive_item(page_id: str) -> dict:
    return notion_repository.archive_page(page_id)
