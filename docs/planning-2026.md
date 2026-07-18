# Planning 2026 API

This API exposes the Notion database `Planeacion 2026` with simple fields intended for AI clients.

All endpoints require `X-API-Key` with the value configured in `NOTION_ADMIN_API_KEY`.

## Data Model

```json
{
  "name": "Comprar escritorio",
  "year": "2026",
  "month": "Abril",
  "tags": ["Cocina"],
  "estimated_budget": 120000,
  "completed": false
}
```

`year`, `month`, and `estimated_budget` may be null. `tags` may be empty.

## CRUD

```bash
curl "http://localhost:8000/planning/items?year=2026&month=Abril" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY"

curl -X POST "http://localhost:8000/planning/items" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Comprar escritorio","month":"Abril","tags":["Cocina"],"estimated_budget":120000}'

curl -X PATCH "http://localhost:8000/planning/items/<page_id>" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

curl -X DELETE "http://localhost:8000/planning/items/<page_id>" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY"
```

`DELETE` archives the Notion page instead of permanently deleting it.

## AI-oriented Views

Get pending items ordered by estimated budget:

```bash
curl "http://localhost:8000/planning/pending?year=2026&limit=20" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY"
```

Get totals grouped by month and tag:

```bash
curl "http://localhost:8000/planning/summary?year=2026" \
  -H "X-API-Key: $NOTION_ADMIN_API_KEY"
```

## Schema Setup

The setup command renames `Checkbox` to `Completado` and ensures that all twelve months exist:

```bash
python -m scripts.setup_planning_2026
```

It is safe to run again: existing month options are preserved and missing options are added.
