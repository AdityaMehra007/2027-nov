import pytest
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient
from omniverse.modules.bangalore.banking import (
    BankCategory,
    BankingCorridor,
    FitoutGrade,
    RegulatoryStatus,
    BangaloreBankOffice,
    GCCCapexOpexModel,
    RBIAuditResult,
    BangaloreBankingEngine,
)
from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine

@pytest.fixture
def mem_session(tmp_path):
    db_file = tmp_path / "banking_mem.db"
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def test_client(tmp_path):
    db_file = tmp_path / "banking_api.db"
    db_engine = DatabaseEngine(f"sqlite:///{db_file}")
    db_engine.init_db()
    app = create_app(db_engine=db_engine)
    with TestClient(app) as client:
        yield client

def test_banking_engine_seeding_and_queries(mem_session):
    engine = BangaloreBankingEngine(mem_session)
    offices = engine.seed_verified_directory()
    assert len(offices) >= 10

    # Query by corridor: Outer Ring Road
    orr_offices = engine.get_offices(corridor=BankingCorridor.OUTER_RING_ROAD)
    assert len(orr_offices) >= 3
    names = [o.name for o in orr_offices]
    assert "Goldman Sachs Bengaluru" in names
    assert "JPMorgan Chase Global Service Center" in names

    # Query by category: PSU Head Office
    psu_hq = engine.get_offices(category=BankCategory.PSU_HEAD_OFFICE)
    assert len(psu_hq) >= 1
    assert psu_hq[0].name == "Canara Bank Global Head Office"
    assert psu_hq[0].corridor == BankingCorridor.CBD_MG_ROAD
    assert psu_hq[0].class_a_vault_installed is True

def test_gcc_capex_opex_calculations(mem_session):
    engine = BangaloreBankingEngine(mem_session)
    model = engine.calculate_gcc_cost_model(
        seats=2000,
        corridor=BankingCorridor.OUTER_RING_ROAD,
        fitout_grade=FitoutGrade.ULTRA_GRADE_A_FINANCIAL
    )
    assert model.seats == 2000
    assert model.super_built_up_sqft == 180000.0
    assert model.capex_civil_fitout_inr_cr > 50.0
    assert model.total_capex_inr_cr > 100.0
    assert model.total_capex_usd_m > 10.0
    assert model.total_annual_opex_inr_cr > 300.0
    assert model.opex_talent_payroll_annual_inr_cr == round((2000 * 1850000.0) / 10000000.0, 2)

def test_rbi_compliance_audit_engine(mem_session):
    engine = BangaloreBankingEngine(mem_session)

    # 1. 100% Compliant Case
    clean_audit = engine.audit_rbi_compliance(
        bank_name="Test Compliant Bank",
        data_localized=True,
        dpdp_consent=True,
        cert_in_6hr=True,
        npl_clock_sync=True,
        vault_cctv_90day=True
    )
    assert clean_audit.overall_score == 100.0
    assert clean_audit.status == RegulatoryStatus.COMPLIANT
    assert len(clean_audit.detected_violations) == 0

    # 2. Critical Breach (Data not localized + missing CERT-In)
    breached_audit = engine.audit_rbi_compliance(
        bank_name="Foreign Bank Branch",
        data_localized=False,
        dpdp_consent=True,
        cert_in_6hr=False,
        npl_clock_sync=True,
        vault_cctv_90day=True
    )
    assert breached_audit.overall_score == 45.0
    assert breached_audit.status == RegulatoryStatus.NON_COMPLIANT
    assert len(breached_audit.detected_violations) == 2
    assert any("CRITICAL: Payment transaction data" in v for v in breached_audit.detected_violations)
    assert any("AWS Mumbai" in p for p in breached_audit.remediation_playbook)

def test_corridor_intelligence(mem_session):
    engine = BangaloreBankingEngine(mem_session)
    intel = engine.get_corridor_intelligence()
    assert "OUTER_RING_ROAD" in intel
    assert "CBD_MG_ROAD" in intel
    assert "WHITEFIELD" in intel
    assert intel["OUTER_RING_ROAD"]["avg_rent_psf"] == 125.0

def test_api_banking_endpoints(test_client):
    # 1. List Offices
    resp = test_client.get("/api/v1/bangalore/banking/offices")
    assert resp.status_code == 200
    offices = resp.json()
    assert len(offices) >= 10

    # 2. Filter by corridor
    resp_orr = test_client.get("/api/v1/bangalore/banking/offices?corridor=OUTER_RING_ROAD")
    assert resp_orr.status_code == 200
    orr_data = resp_orr.json()
    assert len(orr_data) >= 3

    # 3. Corridors
    resp_corr = test_client.get("/api/v1/bangalore/banking/corridors")
    assert resp_corr.status_code == 200
    corr_data = resp_corr.json()
    assert "OUTER_RING_ROAD" in corr_data

    # 4. GCC Blueprint
    blueprint_req = {
        "seats": 1000,
        "corridor": "WHITEFIELD",
        "fitout_grade": "STANDARD_GRADE_A"
    }
    resp_bp = test_client.post("/api/v1/bangalore/banking/gcc-blueprint", json=blueprint_req)
    assert resp_bp.status_code == 200
    bp_data = resp_bp.json()
    assert bp_data["seats"] == 1000
    assert bp_data["corridor"] == "WHITEFIELD"
    assert bp_data["total_capex_inr_cr"] > 0

    # 5. Audit Compliance
    audit_req = {
        "bank_name": "Bengaluru Investment Hub",
        "data_localized": False,
        "dpdp_consent": False,
        "cert_in_6hr": True,
        "npl_clock_sync": True,
        "vault_cctv_90day": True
    }
    resp_audit = test_client.post("/api/v1/bangalore/banking/audit", json=audit_req)
    assert resp_audit.status_code == 200
    audit_data = resp_audit.json()
    assert audit_data["overall_score"] == 45.0
    assert audit_data["status"] == "NON_COMPLIANT"
    assert len(audit_data["detected_violations"]) == 2

    # 6. Branch Network Plans
    resp_branches = test_client.get("/api/v1/bangalore/banking/branches")
    assert resp_branches.status_code == 200
    branch_data = resp_branches.json()
    assert len(branch_data) >= 4
    assert any("Indiranagar" in b["locality"] for b in branch_data)

    # 7. Talent Compensation Matrix
    resp_talent = test_client.get("/api/v1/bangalore/banking/talent")
    assert resp_talent.status_code == 200
    talent_data = resp_talent.json()
    assert len(talent_data) >= 4
    assert any("Quant" in t["role_title"] for t in talent_data)

    # 8. Interactive HTML Dashboard
    resp_dash = test_client.get("/api/v1/bangalore/banking/dashboard")
    assert resp_dash.status_code == 200
    assert "text/html" in resp_dash.headers["content-type"]
    assert "BENGALURU BANKING OPERATIONS" in resp_dash.text

def test_branches_and_talent_benchmarks(mem_session):
    engine = BangaloreBankingEngine(mem_session)
    branches = engine.get_branch_network_plans()
    assert len(branches) >= 4
    indira = [b for b in branches if "Indiranagar" in b.locality][0]
    assert indira.setup_capex_inr_cr == 2.20
    assert "Private Wealth Lounge" in indira.features

    talent = engine.get_talent_benchmarks()
    assert len(talent) >= 4
    sde = [t for t in talent if "SDE" in t.role_title or "Software Development" in t.role_title][0]
    assert sde.fixed_base_inr_lakhs_min >= 14.0
    assert "IIIT-Bangalore" in sde.feeder_institutions
