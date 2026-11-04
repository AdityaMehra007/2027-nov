import pytest
from omniverse.modules.agency.world_clients import (
    GlobalHub,
    IndustrySector,
    WorldClient,
    WorldClientDirectory,
)
from omniverse.modules.agency.models import LeadStage


def test_global_hubs_and_sectors_coverage():
    hubs = list(GlobalHub)
    assert len(hubs) >= 8
    expected_hubs = {
        GlobalHub.SF_BAY_AREA,
        GlobalHub.NEW_YORK,
        GlobalHub.LONDON,
        GlobalHub.BERLIN,
        GlobalHub.SINGAPORE,
        GlobalHub.TOKYO,
        GlobalHub.DUBAI,
        GlobalHub.BENGALURU,
    }
    assert expected_hubs.issubset(set(hubs))

    sectors = list(IndustrySector)
    assert len(sectors) >= 6
    expected_sectors = {
        IndustrySector.SAAS_DEVTOOLS,
        IndustrySector.FINTECH_PAYMENTS,
        IndustrySector.HEALTHCARE_CLINICAL,
        IndustrySector.ECOMMERCE_DTC,
        IndustrySector.CLEANTECH_ENERGY,
        IndustrySector.SMB_SERVICES,
    }
    assert expected_sectors.issubset(set(sectors))


def test_world_client_directory_roster():
    directory = WorldClientDirectory()
    clients = directory.get_all_clients()
    assert len(clients) >= 24

    for client in clients:
        assert isinstance(client, WorldClient)
        assert client.name
        assert client.website.startswith("http")
        assert client.annual_revenue_usd > 50000.0
        assert len(client.tech_stack) >= 2
        assert len(client.declared_needs) >= 1
        assert client.country


def test_directory_filtering():
    directory = WorldClientDirectory()

    sf_clients = directory.filter_clients(hub=GlobalHub.SF_BAY_AREA)
    assert len(sf_clients) >= 3
    for c in sf_clients:
        assert c.hub == GlobalHub.SF_BAY_AREA

    fintech_clients = directory.filter_clients(sector=IndustrySector.FINTECH_PAYMENTS)
    assert len(fintech_clients) >= 3
    for c in fintech_clients:
        assert c.sector == IndustrySector.FINTECH_PAYMENTS

    high_revenue = directory.filter_clients(min_revenue=5_000_000.0)
    assert len(high_revenue) >= 5
    for c in high_revenue:
        assert c.annual_revenue_usd >= 5_000_000.0


def test_find_client_by_name():
    directory = WorldClientDirectory()
    all_clients = directory.get_all_clients()
    sample = all_clients[0]

    found = directory.get_client_by_name(sample.name)
    assert found is not None
    assert found.name == sample.name
    assert found.client_id == sample.client_id

    missing = directory.get_client_by_name("NonExistentCorporationXYZ")
    assert missing is None


def test_convert_to_crm_leads():
    directory = WorldClientDirectory()
    leads = directory.to_crm_leads(limit=10)
    assert len(leads) == 10
    for lead in leads:
        assert lead.business_name
        assert lead.stage == LeadStage.DISCOVERED
        assert lead.estimated_annual_revenue_usd > 0.0
