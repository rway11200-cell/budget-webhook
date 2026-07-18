from app.coding_loop import repository

TASK_STATUS_TO_NOTION = {"In Progress": "in Progress"}
TASK_STATUS_FROM_NOTION = {value: key for key, value in TASK_STATUS_TO_NOTION.items()}


def _title(value: str) -> dict:
    return {"title": [{"text": {"content": value}}]}


def _rich_text(value: str | None) -> dict:
    return {"rich_text": [{"text": {"content": value}}] if value else []}


def _select(value: str | None) -> dict:
    return {"select": {"name": value} if value else None}


def _date(value: str | None) -> dict:
    return {"date": {"start": value} if value else None}


def _relation(value: str | None) -> dict:
    return {"relation": [{"id": value}] if value else []}


def _plain_text(items: list[dict]) -> str:
    return "".join(item.get("plain_text", "") for item in items)


def _select_name(prop: dict) -> str | None:
    value = prop.get("select")
    return value.get("name") if value else None


def _date_start(prop: dict) -> str | None:
    value = prop.get("date")
    return value.get("start") if value else None


def _relation_id(prop: dict) -> str | None:
    values = prop.get("relation", [])
    return values[0].get("id") if values else None


def _metadata(page: dict) -> dict:
    return {
        "id": page.get("id", ""),
        "url": page.get("url"),
        "created_time": page.get("created_time"),
        "last_edited_time": page.get("last_edited_time"),
    }


def _project_properties(data, partial: bool) -> dict:
    values = data.model_dump(exclude_unset=partial)
    mapping = {
        "project": ("Project", lambda value: _title(value)),
        "auto_commit": ("Auto commit", lambda value: {"checkbox": value}),
        "branch": ("Branch", _rich_text),
        "opencode_session": ("OpenCode Sesion", _rich_text),
        "priority": ("Priority", _select),
        "repo_path": ("Repo Path", lambda value: {"url": value}),
        "status": ("Status", _select),
        "updated": ("Updated", _date),
    }
    return _map_properties(values, mapping, {"project", "auto_commit", "status"})


def _task_properties(data, partial: bool) -> dict:
    values = data.model_dump(exclude_unset=partial)
    if values.get("status") in TASK_STATUS_TO_NOTION:
        values["status"] = TASK_STATUS_TO_NOTION[values["status"]]
    mapping = {
        "task": ("Task", lambda value: _title(value)),
        "approved": ("Approved", lambda value: {"checkbox": value}),
        "attempts": ("Attempts", lambda value: {"number": value}),
        "created": ("Created", _date),
        "last_result": ("Last result", _rich_text),
        "next_actions": ("Next actions", _rich_text),
        "priority": ("Priority", _select),
        "project_id": ("Project", _relation),
        "status": ("Status", _select),
        "updated": ("Updated", _date),
    }
    return _map_properties(values, mapping, {"task", "approved", "status"})


def _run_properties(data, partial: bool) -> dict:
    values = data.model_dump(exclude_unset=partial)
    mapping = {
        "run_id": ("Run ID", lambda value: _title(value)),
        "duration": ("Duration", lambda value: {"number": value}),
        "openai_available": ("OpenIA available", lambda value: {"checkbox": value}),
        "status": ("Status", _select),
        "summary": ("Summary", _rich_text),
        "task_id": ("Task", _relation),
        "timestamp": ("Timestamp", _date),
    }
    return _map_properties(values, mapping, {"run_id", "openai_available"})


def _test_error_properties(data, partial: bool) -> dict:
    values = data.model_dump(exclude_unset=partial)
    mapping = {
        "run_id": ("Run ID", lambda value: _title(value)),
        "duration": ("Duration", lambda value: {"number": value}),
        "status": ("Status", _select),
        "summary": ("Summary", _rich_text),
        "timestamp": ("Timestamp", _date),
    }
    return _map_properties(values, mapping, {"run_id"})


def _map_properties(values: dict, mapping: dict, non_nullable: set[str]) -> dict:
    props = {}
    for field, value in values.items():
        if field in non_nullable and value is None:
            raise ValueError(f"{field} cannot be null")
        property_name, formatter = mapping[field]
        props[property_name] = formatter(value)
    return props


def _to_project(page: dict) -> dict:
    props = page.get("properties", {})
    return {
        **_metadata(page),
        "project": _plain_text(props.get("Project", {}).get("title", [])),
        "auto_commit": bool(props.get("Auto commit", {}).get("checkbox", False)),
        "branch": _plain_text(props.get("Branch", {}).get("rich_text", [])) or None,
        "opencode_session": _plain_text(props.get("OpenCode Sesion", {}).get("rich_text", [])) or None,
        "priority": _select_name(props.get("Priority", {})),
        "repo_path": props.get("Repo Path", {}).get("url"),
        "status": _select_name(props.get("Status", {})) or "Active",
        "updated": _date_start(props.get("Updated", {})),
    }


def _to_task(page: dict) -> dict:
    props = page.get("properties", {})
    status = _select_name(props.get("Status", {})) or "To-do"
    return {
        **_metadata(page),
        "task": _plain_text(props.get("Task", {}).get("title", [])),
        "approved": bool(props.get("Approved", {}).get("checkbox", False)),
        "attempts": props.get("Attempts", {}).get("number"),
        "created": _date_start(props.get("Created", {})),
        "last_result": _plain_text(props.get("Last result", {}).get("rich_text", [])) or None,
        "next_actions": _plain_text(props.get("Next actions", {}).get("rich_text", [])) or None,
        "priority": _select_name(props.get("Priority", {})),
        "project_id": _relation_id(props.get("Project", {})),
        "status": TASK_STATUS_FROM_NOTION.get(status, status),
        "updated": _date_start(props.get("Updated", {})),
    }


def _to_run(page: dict) -> dict:
    props = page.get("properties", {})
    return {
        **_metadata(page),
        "run_id": _plain_text(props.get("Run ID", {}).get("title", [])),
        "duration": props.get("Duration", {}).get("number"),
        "openai_available": bool(props.get("OpenIA available", {}).get("checkbox", False)),
        "status": _select_name(props.get("Status", {})),
        "summary": _plain_text(props.get("Summary", {}).get("rich_text", [])) or None,
        "task_id": _relation_id(props.get("Task", {})),
        "timestamp": _date_start(props.get("Timestamp", {})),
    }


def _to_test_error(page: dict) -> dict:
    props = page.get("properties", {})
    return {
        **_metadata(page),
        "run_id": _plain_text(props.get("Run ID", {}).get("title", [])),
        "duration": props.get("Duration", {}).get("number"),
        "status": _select_name(props.get("Status", {})),
        "summary": _plain_text(props.get("Summary", {}).get("rich_text", [])) or None,
        "timestamp": _date_start(props.get("Timestamp", {})),
    }


CONFIG = {
    "projects": (_project_properties, _to_project, "Status"),
    "tasks": (_task_properties, _to_task, "Status"),
    "runs": (_run_properties, _to_run, "Status"),
    "test-errors": (_test_error_properties, _to_test_error, "Status"),
}


def list_records(
    resource: str,
    status: str | None,
    relation_property: str | None,
    relation_id: str | None,
    checkbox_property: str | None,
    checkbox_value: bool | None,
    page_size: int,
    start_cursor: str | None,
) -> dict:
    _, converter, status_property = CONFIG[resource]
    filters = []
    if status:
        notion_status = TASK_STATUS_TO_NOTION.get(status, status)
        filters.append({"property": status_property, "select": {"equals": notion_status}})
    if relation_property and relation_id:
        filters.append({"property": relation_property, "relation": {"contains": relation_id}})
    if checkbox_property and checkbox_value is not None:
        filters.append(
            {"property": checkbox_property, "checkbox": {"equals": checkbox_value}}
        )

    payload = {"page_size": page_size}
    if len(filters) == 1:
        payload["filter"] = filters[0]
    elif filters:
        payload["filter"] = {"and": filters}
    if start_cursor:
        payload["start_cursor"] = start_cursor

    result = repository.query(resource, payload)
    return {
        "items": [converter(page) for page in result.get("results", [])],
        "next_cursor": result.get("next_cursor"),
        "has_more": result.get("has_more", False),
    }


def create_record(resource: str, data) -> dict:
    property_builder, converter, _ = CONFIG[resource]
    return converter(repository.create(resource, property_builder(data, False)))


def get_record(resource: str, page_id: str) -> dict:
    _, converter, _ = CONFIG[resource]
    return converter(repository.get(page_id))


def update_record(resource: str, page_id: str, data) -> dict:
    property_builder, converter, _ = CONFIG[resource]
    properties = property_builder(data, True)
    if not properties:
        raise ValueError("At least one field is required")
    return converter(repository.update(page_id, properties))


def delete_record(page_id: str) -> dict:
    page = repository.archive(page_id)
    return {"id": page.get("id", page_id), "archived": page.get("archived", True)}
