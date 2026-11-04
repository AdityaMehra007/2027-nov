import pytest
from omniverse.modules.commerce.models import BusinessUnitID, BusinessUnitSpec
from omniverse.modules.commerce.catalog import CommerceMatrix

def test_commerce_matrix_all_10_units():
    matrix = CommerceMatrix()
    units = matrix.list_all_units()
    
    assert len(units) == 10
    unit_ids = {u.unit_id for u in units}
    
    expected_units = {
        BusinessUnitID.AI_SERVICE_AGENCY,
        BusinessUnitID.SAAS_FACTORY,
        BusinessUnitID.DATA_INTELLIGENCE_SERVICES,
        BusinessUnitID.DEVELOPER_API_BUSINESS,
        BusinessUnitID.DIGITAL_PRODUCT_BUSINESS,
        BusinessUnitID.MARKET_INTELLIGENCE_SUBSCRIPTIONS,
        BusinessUnitID.ENTERPRISE_TECHNOLOGY,
        BusinessUnitID.MARKETPLACE,
        BusinessUnitID.CONSULTANCY_AND_IMPLEMENTATION,
        BusinessUnitID.PARTNERSHIP_AND_REFERRAL
    }
    assert unit_ids == expected_units

def test_commerce_matrix_projected_margins():
    matrix = CommerceMatrix()
    summary = matrix.calculate_portfolio_economics()
    
    assert summary["total_business_units"] == 10
    assert summary["average_gross_margin_pct"] >= 70.0
    assert "projected_annual_capacity_inr" in summary
