# Request Flow

```
Tasker (Android) → HTTP GET → FastAPI route → Service parses notification
→ Repository (Notion API) → Repository (Telegram API) → User
```

```mermaid
flowchart TD
    A[Tasker captura notificación] --> B[HTTP GET con ?text=...]
    B --> C[FastAPI route en app/tasker/routes.py]
    C --> D[Service parsea CMR o Scotia]
    D --> E[Repository registra en Notion DB Movimientos]
    E --> F[Repository envía resumen a Telegram]
    F --> G[Usuario ve saldo disponible]
```

## Layers

- **`routes.py`** — recibe la petición HTTP, extrae query params, retorna respuestas.
- **`schemas.py`** — modelos Pydantic para validación y documentación OpenAPI.
- **`service.py`** — lógica de aplicación: parseo de notificaciones, inferencia de categorías, cálculo de presupuesto.
- **`repository.py`** — integraciones externas: API de Notion (gastos y periodos), API de Telegram (mensajes).
- **`config.py`** — variables de entorno centralizadas.
