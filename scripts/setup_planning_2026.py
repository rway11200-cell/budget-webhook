from app.config import PLANNING_2026_DATABASE_ID
from app.notion import repository

MONTHS = [
    ("Enero", "brown"),
    ("Febrero", "gray"),
    ("Marzo", "orange"),
    ("Abril", "yellow"),
    ("Mayo", "green"),
    ("Junio", "pink"),
    ("Julio", "blue"),
    ("Agosto", "purple"),
    ("Septiembre", "red"),
    ("Octubre", "brown"),
    ("Noviembre", "gray"),
    ("Diciembre", "green"),
]


def run():
    database = repository.get_database(PLANNING_2026_DATABASE_ID)
    properties = database.get("properties", {})

    if "Checkbox" in properties:
        repository.update_database(
            PLANNING_2026_DATABASE_ID,
            {"properties": {"Checkbox": {"name": "Completado"}}},
        )

    month_options = properties.get("Mes", {}).get("select", {}).get("options", [])
    existing_by_name = {option["name"]: option for option in month_options}
    options = []
    for name, color in MONTHS:
        existing = existing_by_name.get(name)
        if existing:
            options.append(
                {"id": existing["id"], "name": existing["name"], "color": existing["color"]}
            )
        else:
            options.append({"name": name, "color": color})

    repository.update_database(
        PLANNING_2026_DATABASE_ID,
        {"properties": {"Mes": {"select": {"options": options}}}},
    )
    print("Planeación 2026 schema updated")


if __name__ == "__main__":
    run()
