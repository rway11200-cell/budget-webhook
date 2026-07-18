# Autonomous Coding Loop API

Typed access to the four databases nested under the Notion page `Autonomous Coding Loop`:

- Projects
- Tasks
- Run Log
- Run Test Error

All endpoints require `X-API-Key` with the value configured in `NOTION_ADMIN_API_KEY`.

## Projects

```bash
curl "http://localhost:8000/coding-loop/projects?status=Active" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY"

curl -X POST "http://localhost:8000/coding-loop/projects" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project":"Nexo","repo_path":"https://github.com/example/nexo","priority":"High","status":"Active"}'
```

## Tasks

Get tasks ready and approved for autonomous execution:

```bash
curl "http://localhost:8000/coding-loop/tasks?status=Ready&approved=true" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY"
```

Create a task related to a project:

```bash
curl -X POST "http://localhost:8000/coding-loop/tasks" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task":"Implement endpoint","project_id":"<project_page_id>","priority":"High","status":"Ready","approved":true}'
```

## Runs

```bash
curl "http://localhost:8000/coding-loop/runs?task_id=<task_page_id>" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY"

curl -X POST "http://localhost:8000/coding-loop/runs" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"run_id":"run-20260718-120000","task_id":"<task_page_id>","status":"Running","openai_available":true}'
```

## Test Errors

```bash
curl "http://localhost:8000/coding-loop/test-errors?status=Failed" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY"
```

Each resource supports the same CRUD pattern:

```text
GET    /coding-loop/<resource>
POST   /coding-loop/<resource>
GET    /coding-loop/<resource>/<page_id>
PATCH  /coding-loop/<resource>/<page_id>
DELETE /coding-loop/<resource>/<page_id>
```

`DELETE` archives the underlying Notion page.
