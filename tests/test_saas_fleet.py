import pytest
from fastapi.testclient import TestClient
from omniverse.modules.saas.fleet import VerticalSaaSFleetEngine, SaaSVertical, SaaSPlan
from omniverse.api.app import create_app

def test_saas_fleet_engine_operations():
    engine = VerticalSaaSFleetEngine()
    
    # 1. Verification of seeded tenants
    tenants = engine.list_tenants()
    assert len(tenants) >= 4
    
    summary = engine.calculate_fleet_summary()
    assert summary["total_subscribers"] >= 4
    assert summary["total_mrr_usd"] > 0
    assert summary["total_arr_usd"] > 0
    assert "CLOUDBITE" in summary["verticals"]
    assert "GYMVERSE" in summary["verticals"]

    # 2. Provisioning new tenant
    new_tenant = engine.provision_tenant(
        name="Urban Slice Pizza",
        vertical=SaaSVertical.CLOUDBITE,
        plan=SaaSPlan.ENTERPRISE
    )
    assert new_tenant.name == "Urban Slice Pizza"
    assert new_tenant.mrr_usd == 249.0
    assert new_tenant.api_key.startswith("omni_live_")
    assert engine.get_tenant(new_tenant.tenant_id) is not None

def test_vertical_domain_logic():
    engine = VerticalSaaSFleetEngine()
    
    # CloudBite food margin
    cb = engine.cloudbite_calculate_recipe_margin(selling_price=100.0, ingredient_costs=[20.0, 5.0, 5.0])
    assert cb["food_cost_pct"] == 30.0
    assert cb["status"] == "HEALTHY"

    # GymVerse retention
    gv = engine.gymverse_assess_member_retention(checkins_last_30d=12, auto_pay_active=True)
    assert gv["retention_score"] >= 75.0
    assert gv["churn_risk"] == "LOW"

    # RentShield risk scoring
    rs_pass = engine.rentshield_evaluate_tenant_risk(monthly_rent=30000.0, declared_monthly_income=120000.0, credit_score=780)
    assert rs_pass["decision"] == "APPROVED_ZERO_DEPOSIT"

    rs_fail = engine.rentshield_evaluate_tenant_risk(monthly_rent=70000.0, declared_monthly_income=100000.0, credit_score=580)
    assert rs_fail["decision"] == "REJECTED_HIGH_RISK"

    # ClinicFlow triage
    cf_emerg = engine.clinicflow_triage_symptom(symptoms=["Severe chest pain"], severity_1_to_10=9)
    assert cf_emerg["priority"] == "IMMEDIATE_ER"

def test_saas_fleet_api_endpoints():
    app = create_app()
    client = TestClient(app)

    # 1. Summary
    res = client.get("/api/v1/saas/fleet/summary")
    assert res.status_code == 200
    data = res.json()
    assert "total_mrr_usd" in data
    assert "verticals" in data

    # 2. Provisioning API
    res_prov = client.post("/api/v1/saas/fleet/provision", json={
        "name": "Zenith Dental Studio",
        "vertical": "CLINICFLOW",
        "plan": "GROWTH"
    })
    assert res_prov.status_code == 200
    tenant_data = res_prov.json()
    assert tenant_data["name"] == "Zenith Dental Studio"
    assert tenant_data["vertical"] == "CLINICFLOW"

    # 3. Filter tenants by vertical
    res_list = client.get("/api/v1/saas/fleet/tenants?vertical=CLINICFLOW")
    assert res_list.status_code == 200
    clinics = res_list.json()
    assert len(clinics) >= 2
    assert all(c["vertical"] == "CLINICFLOW" for c in clinics)

    # 4. Domain endpoints
    res_cb = client.post("/api/v1/saas/fleet/cloudbite/margin", json={
        "selling_price": 500.0,
        "ingredient_costs": [120.0, 30.0],
        "labor_overhead": 50.0
    })
    assert res_cb.status_code == 200
    assert res_cb.json()["food_cost_pct"] == 30.0
