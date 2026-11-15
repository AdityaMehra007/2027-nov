import os
from pathlib import Path
from omniverse.modules.opportunities.beachhead import BeachheadAuditGenerator

generator = BeachheadAuditGenerator()
deliverable = generator.generate_audit(
    prospect_name="Apex Logistics India",
    industry="Logistics & Freight Forwarding",
    current_workflow="Manual freight bill entry, multi-vendor rate reconciliation, and POD verification",
    monthly_volume=2500,
    human_hours_per_unit=0.25,
    hourly_wage_usd=15.0,
    proposed_monthly_fee_usd=149.0,
)

out_dir = Path("reports/audits")
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / "apex_logistics_audit_sample.md"

with open(out_file, "w", encoding="utf-8") as f:
    f.write(deliverable.markdown_report)

print(f"Generated {out_file} successfully! ROI: {deliverable.roi_percentage}%")
