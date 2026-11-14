import pytest
from src.nexus.departments import (
    DepartmentEnum,
    CapabilityDescriptor,
    CapabilityRegistry,
    get_all_capabilities,
    get_capability_by_id,
)

def test_departments_enum():
    departments = list(DepartmentEnum)
    assert len(departments) == 9
    names = [d.name for d in departments]
    assert "DEPT_A" in names  # Universal Intelligence
    assert "DEPT_B" in names  # Science and Frontier Technology
    assert "DEPT_C" in names  # Computational and Engineering
    assert "DEPT_D" in names  # Business and Economics
    assert "DEPT_E" in names  # Knowledge and Education
    assert "DEPT_F" in names  # World and Infrastructure
    assert "DEPT_G" in names  # Creation and Execution
    assert "DEPT_H" in names  # Control and Governance
    assert "DEPT_I" in names  # Advanced Intelligence

def test_all_50_capabilities_registered():
    caps = get_all_capabilities()
    assert len(caps) == 50, f"Expected 50 capabilities, got {len(caps)}"
    
    # Assert IDs 1 through 50 are present
    ids = {c.id for c in caps}
    for i in range(1, 51):
        assert i in ids, f"Capability {i} missing from catalog"

def test_capability_lookup():
    cap1 = get_capability_by_id(1)
    assert cap1 is not None
    assert cap1.name == "Universal Intelligence Engine"
    assert cap1.department == DepartmentEnum.DEPT_A

    cap36 = get_capability_by_id(36)
    assert cap36 is not None
    assert cap36.name == "Product Foundry"
    assert cap36.department == DepartmentEnum.DEPT_G

    # Missing capability
    assert get_capability_by_id(999) is None

def test_filter_by_department():
    registry = CapabilityRegistry()
    dept_a_caps = registry.filter_by_department(DepartmentEnum.DEPT_A)
    assert len(dept_a_caps) == 5  # Capabilities 1 through 5

    dept_b_caps = registry.filter_by_department(DepartmentEnum.DEPT_B)
    assert len(dept_b_caps) == 10  # Capabilities 6 through 15
