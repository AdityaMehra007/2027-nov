# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Test suite for Deliverables Builder generating all 30 canonical Project One deliverables."""

import pytest
from pathlib import Path
from omniverse.modules.opportunities.deliverables_builder import DeliverablesBuilder


def test_build_all_30_deliverables(tmp_path):
    """Verify that all 30 canonical deliverables specified in Part 21 are generated."""
    builder = DeliverablesBuilder()
    output_dir = tmp_path / "deliverables"
    
    generated_files = builder.build_all(output_dir)
    assert len(generated_files) == 30

    for idx, path in enumerate(generated_files, start=1):
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert len(content) > 200
        assert "# " in content
        assert "PROJECT ONE" in content or "OMNIVERSE" in content

    # Check specific milestone deliverables
    file_names = {p.name for p in generated_files}
    assert "01_TECHNICAL_ARCHITECTURE.md" in file_names
    assert "02_GLOBAL_RESEARCH_REPORT.md" in file_names
    assert "03_CUSTOMER_SEGMENTATION_DATABASE.md" in file_names
    assert "06_REVENUE_MODEL_CATALOGUE.md" in file_names
    assert "11_OPPORTUNITY_RANKING.md" in file_names
    assert "15_CUSTOMER_PORTAL.md" in file_names
    assert "20_SECURITY_DOCUMENTATION.md" in file_names
    assert "30_FIRST_PAID_PILOT_PLAN.md" in file_names
