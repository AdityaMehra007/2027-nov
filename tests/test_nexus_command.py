import pytest
from src.nexus.command import NexusCommandCenter, ProjectDirective
from src.nexus.departments import DepartmentEnum

def test_command_center_intake_basic():
    center = NexusCommandCenter()
    directive = center.parse_intake(
        raw_input="Build a quantum error correction simulation and test surface codes",
        user_id="aditya"
    )
    assert isinstance(directive, ProjectDirective)
    assert directive.directive_id.startswith("DIR-")
    assert directive.user_id == "aditya"
    assert DepartmentEnum.DEPT_B in directive.target_departments
    assert 8 in directive.requested_capabilities  # Quantum Intelligence

def test_command_center_intake_software_factory():
    center = NexusCommandCenter()
    directive = center.parse_intake(
        raw_input="Generate a full stack saas application with automated tests",
        user_id="aditya"
    )
    assert DepartmentEnum.DEPT_G in directive.target_departments or DepartmentEnum.DEPT_C in directive.target_departments
    assert (18 in directive.requested_capabilities) or (40 in directive.requested_capabilities)

def test_command_center_intake_everything():
    center = NexusCommandCenter()
    directive = center.parse_intake(
        raw_input="Make the level very high make it everything so I can create everything omniverse civilization scale",
        user_id="aditya"
    )
    # When "everything" / "civilization" / "omniverse" is requested, all 9 departments should be targeted
    assert len(directive.target_departments) == 9
    assert len(directive.requested_capabilities) == 50

def test_command_center_empty_input_validation():
    center = NexusCommandCenter()
    with pytest.raises(ValueError, match="Input directive cannot be empty"):
        center.parse_intake("   ")

def test_command_center_list_capabilities():
    center = NexusCommandCenter()
    caps = center.list_capabilities()
    assert len(caps) == 50
    cap8 = center.get_capability(8)
    assert cap8.name == "Quantum Intelligence"
