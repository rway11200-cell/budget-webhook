from app.main import app
from app.tasker import service
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "budget-webhook"


def test_status():
    resp = client.get("/status")
    assert resp.status_code == 200
    data = resp.json()
    for key in ("spent", "remaining", "budget", "day", "days_total", "month_pct", "spent_pct", "pace", "advice"):
        assert key in data


def test_status_text():
    resp = client.get("/status/text")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/plain")


def test_tasker_no_text():
    resp = client.get("/tasker")
    assert resp.status_code == 200
    assert resp.json() == {"ok": False, "reason": "no text"}


def test_tasker_cmr():
    text = "Compraste $1.500 en Starbucks SANTIAGO/CHL Con tu CMR"
    resp = client.get(f"/tasker?text={text}")
    assert resp.status_code == 200
    data = resp.json()
    if "ok" not in data:
        assert "spent" in data
        assert "remaining" in data


def test_tasker_cmr_not_matched():
    resp = client.get("/tasker/cmr?text=noticias%20del%20dia")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True, "reason": "not a CMR purchase"}


def test_tasker_scotiabank_not_matched():
    resp = client.get("/tasker/scotiabank?text=hola%20mundo")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True, "reason": "not a Scotia expense"}


def test_test_telegram_no_token():
    resp = client.get("/test-telegram")
    assert resp.status_code == 400
    assert "error" in resp.json()


def test_parse_cmr():
    result = service.parse_cmr("Compraste $1.500 en Starbucks SANTIAGO/CHL Con tu CMR")
    assert result is not None
    assert result["amount"] == 1500
    assert result["merchant"] == "Starbucks"


def test_parse_cmr_with_decimal():
    result = service.parse_cmr("Compraste $15.990 en MERCADO LIBRE SANTIAGO/CHL ...")
    assert result is not None
    assert result["amount"] == 15990


def test_parse_scotiabank():
    result = service.parse_scotiabank("App Scotia. Se realizó un pago ... por $25.000 en NETFLIX.")
    assert result is not None
    assert result["amount"] == 25000
    assert result["merchant"] == "NETFLIX"


def test_infer_category():
    assert service.infer_category("Starbucks") == "comida"
    assert service.infer_category("ZARA") == "vestuario"
    assert service.infer_category("COPEC") == "auto"
    assert service.infer_category("Desconocido SA") == "otro"


def test_clean_text():
    assert service.clean_text("hola%20mundo%evtprm1") == "holamundo"
    assert service.clean_text("%NTITLE%NTEXT") == ""


def test_openapi_spec():
    spec = app.openapi()
    assert spec["info"]["title"] == "Budget Webhook API"
    assert "/tasker" in spec["paths"]
    assert "/health" in spec["paths"]


def test_get_budget_summary():
    summary = service.get_budget_summary(budget=1000000)
    assert summary["budget"] == 1000000
    assert summary["remaining"] == 1000000 - summary["spent"]
    assert "advice" in summary
