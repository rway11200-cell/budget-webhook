from collections import defaultdict

from app.planning import repository

PROPERTY_NAME = "Name"
PROPERTY_YEAR = "Año"
PROPERTY_MONTH = "Mes"
PROPERTY_TAGS = "Tag"
PROPERTY_BUDGET = "Valor Estimado o Presupuesto"
PROPERTY_COMPLETED = "Completado"


def _title_value(value: str) -> dict:
    return {"title": [{"text": {"content": value}}]}


def _select_value(value: str | None) -> dict:
    return {"select": {"name": value} if value else None}


def _to_properties(data, partial: bool = False) -> dict:
    values = data.model_dump(exclude_unset=partial)
    properties = {}

    if "name" in values:
        if values["name"] is None:
            raise ValueError("name cannot be null")
        properties[PROPERTY_NAME] = _title_value(values["name"])
    if "year" in values:
        properties[PROPERTY_YEAR] = _select_value(values["year"])
    if "month" in values:
        properties[PROPERTY_MONTH] = _select_value(values["month"])
    if "tags" in values:
        if values["tags"] is None:
            raise ValueError("tags cannot be null")
        properties[PROPERTY_TAGS] = {
            "multi_select": [{"name": tag} for tag in values["tags"]]
        }
    if "estimated_budget" in values:
        properties[PROPERTY_BUDGET] = {"number": values["estimated_budget"]}
    if "completed" in values:
        if values["completed"] is None:
            raise ValueError("completed cannot be null")
        properties[PROPERTY_COMPLETED] = {"checkbox": values["completed"]}

    return properties


def _rich_text(value: list[dict]) -> str:
    return "".join(item.get("plain_text", "") for item in value)


def _to_item(page: dict) -> dict:
    properties = page.get("properties", {})
    title = properties.get(PROPERTY_NAME, {}).get("title", [])
    year = properties.get(PROPERTY_YEAR, {}).get("select")
    month = properties.get(PROPERTY_MONTH, {}).get("select")
    tags = properties.get(PROPERTY_TAGS, {}).get("multi_select", [])

    return {
        "id": page.get("id", ""),
        "name": _rich_text(title),
        "year": year.get("name") if year else None,
        "month": month.get("name") if month else None,
        "tags": [tag.get("name", "") for tag in tags],
        "estimated_budget": properties.get(PROPERTY_BUDGET, {}).get("number"),
        "completed": bool(properties.get(PROPERTY_COMPLETED, {}).get("checkbox", False)),
        "url": page.get("url"),
        "created_time": page.get("created_time"),
        "last_edited_time": page.get("last_edited_time"),
    }


def _build_filter(
    year: str | None = None,
    month: str | None = None,
    tag: str | None = None,
    completed: bool | None = None,
) -> dict | None:
    filters = []
    if year:
        filters.append({"property": PROPERTY_YEAR, "select": {"equals": year}})
    if month:
        filters.append({"property": PROPERTY_MONTH, "select": {"equals": month}})
    if tag:
        filters.append({"property": PROPERTY_TAGS, "multi_select": {"contains": tag}})
    if completed is not None:
        filters.append({"property": PROPERTY_COMPLETED, "checkbox": {"equals": completed}})

    if not filters:
        return None
    if len(filters) == 1:
        return filters[0]
    return {"and": filters}


def list_items(
    year: str | None,
    month: str | None,
    tag: str | None,
    completed: bool | None,
    page_size: int,
    start_cursor: str | None,
) -> dict:
    payload = {"page_size": page_size}
    item_filter = _build_filter(year, month, tag, completed)
    if item_filter:
        payload["filter"] = item_filter
    if start_cursor:
        payload["start_cursor"] = start_cursor

    result = repository.query_items(payload)
    return {
        "items": [_to_item(page) for page in result.get("results", [])],
        "next_cursor": result.get("next_cursor"),
        "has_more": result.get("has_more", False),
    }


def create_item(data) -> dict:
    return _to_item(repository.create_item(_to_properties(data)))


def get_item(page_id: str) -> dict:
    return _to_item(repository.get_item(page_id))


def update_item(page_id: str, data) -> dict:
    properties = _to_properties(data, partial=True)
    if not properties:
        raise ValueError("At least one field is required")
    return _to_item(repository.update_item(page_id, properties))


def delete_item(page_id: str) -> dict:
    page = repository.archive_item(page_id)
    return {"id": page.get("id", page_id), "archived": page.get("archived", True)}


def _all_items(
    year: str | None = None,
    month: str | None = None,
    tag: str | None = None,
    completed: bool | None = None,
    sorts: list[dict] | None = None,
) -> list[dict]:
    items = []
    cursor = None
    item_filter = _build_filter(year, month, tag, completed)

    while True:
        payload = {"page_size": 100}
        if item_filter:
            payload["filter"] = item_filter
        if sorts:
            payload["sorts"] = sorts
        if cursor:
            payload["start_cursor"] = cursor

        result = repository.query_items(payload)
        items.extend(_to_item(page) for page in result.get("results", []))
        if not result.get("has_more"):
            return items
        cursor = result.get("next_cursor")


def pending_items(
    year: str | None,
    month: str | None,
    tag: str | None,
    limit: int,
) -> list[dict]:
    items = _all_items(
        year,
        month,
        tag,
        completed=False,
        sorts=[{"property": PROPERTY_BUDGET, "direction": "descending"}],
    )
    return items[:limit]


def _group_summary(items: list[dict], field: str, empty_name: str) -> list[dict]:
    groups = defaultdict(lambda: {"item_count": 0, "completed_count": 0, "estimated_budget": 0.0})

    for item in items:
        names = item[field] if isinstance(item[field], list) else [item[field] or empty_name]
        if not names:
            names = [empty_name]
        for name in names:
            group = groups[name]
            group["item_count"] += 1
            group["completed_count"] += int(item["completed"])
            group["estimated_budget"] += item["estimated_budget"] or 0

    return [
        {"name": name, **values}
        for name, values in sorted(groups.items(), key=lambda pair: pair[0])
    ]


def get_summary(year: str | None, month: str | None, tag: str | None) -> dict:
    items = _all_items(year, month, tag)
    completed_items = [item for item in items if item["completed"]]
    pending_items_list = [item for item in items if not item["completed"]]

    return {
        "item_count": len(items),
        "completed_count": len(completed_items),
        "pending_count": len(pending_items_list),
        "estimated_budget": sum(item["estimated_budget"] or 0 for item in items),
        "completed_budget": sum(item["estimated_budget"] or 0 for item in completed_items),
        "pending_budget": sum(item["estimated_budget"] or 0 for item in pending_items_list),
        "by_month": _group_summary(items, "month", "Sin mes"),
        "by_tag": _group_summary(items, "tags", "Sin tag"),
    }
