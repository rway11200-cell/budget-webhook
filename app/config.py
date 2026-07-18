import os

from dotenv import load_dotenv

load_dotenv()

NOTION_API_TOKEN = os.environ.get("NOTION_API_TOKEN", "")
NOTION_ADMIN_API_KEY = os.environ.get("NOTION_ADMIN_API_KEY", "")
PLANNING_2026_DATABASE_ID = os.environ.get(
    "PLANNING_2026_DATABASE_ID",
    "2d406589-4ee5-8035-987f-d110e5d30e3d",
)
CODING_LOOP_PROJECTS_DATABASE_ID = os.environ.get(
    "CODING_LOOP_PROJECTS_DATABASE_ID",
    "39b06589-4ee5-8068-b292-f3a7e1e60bb2",
)
CODING_LOOP_TASKS_DATABASE_ID = os.environ.get(
    "CODING_LOOP_TASKS_DATABASE_ID",
    "39b06589-4ee5-80ca-85a4-c7387330180c",
)
CODING_LOOP_RUNS_DATABASE_ID = os.environ.get(
    "CODING_LOOP_RUNS_DATABASE_ID",
    "39b06589-4ee5-8032-99ad-d902b29028ba",
)
CODING_LOOP_ERRORS_DATABASE_ID = os.environ.get(
    "CODING_LOOP_ERRORS_DATABASE_ID",
    "3a106589-4ee5-8037-93b9-daaa5e5c2686",
)
MOVIMIENTOS_DB = os.environ.get("MOVIMIENTOS_DB", "")
PERIODO_DB = os.environ.get("PERIODO_DB", "39d06589-4ee5-8036-a3ef-c73eadeae4f8")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_GROUP_ID = os.environ.get("TELEGRAM_GROUP_ID", "")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
