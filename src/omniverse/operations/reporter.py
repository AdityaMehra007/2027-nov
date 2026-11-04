from pathlib import Path
import time
from datetime import datetime
from sqlmodel import Session
from omniverse.core.config import get_settings
from omniverse.operations.health import HealthDiagnostics
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.modules.markets.engine import MultiMarketEngine
from omniverse.modules.commerce.catalog import CommerceMatrix

class ExecutiveReportGenerator:
    """Compiles unified daily briefings of platform financials, pipeline status,

    multi-market intelligence, and system health.
    """

    def __init__(self, session: Session, output_dir: Path | None = None):
        self.session = session
        self.output_dir = Path(output_dir) if output_dir else Path("./reports/executive_briefs")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_daily_brief(self) -> Path:
        settings = get_settings()
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = self.output_dir / f"daily_brief_{date_str}.md"

        diagnostics = HealthDiagnostics(self.session).run_diagnostics()
        pipeline_sum = LeadPipeline(self.session).get_pipeline_summary()
        ledger = PaymentWorkflow(self.session).get_financial_ledger()
        quotes = MultiMarketEngine().get_global_overview()
        commerce = CommerceMatrix().calculate_portfolio_economics()

        quotes_table = "\n".join([f"| {q.symbol} | {q.asset_class.value} | {q.price} {q.currency} | {q.change_24h_pct:+0.2f}% |" for q in quotes[:5]])

        content = f"""# CASHFLOW INFINITY: OMNIVERSE
## DAILY EXECUTIVE BRIEFING — {date_str}

**Platform Version:** {settings.version}  
**Primary Hub:** {settings.primary_market}  
**Generated At:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}  

---

### 💰 1. Financial Ledger & Revenue Reconciliation
- **Confirmed Collected Revenue**: ₹{ledger['collected_revenue_inr']:,.2f}
- **Outstanding Receivables**: ₹{ledger['outstanding_receivables_inr']:,.2f}
- **Active Pipeline Gross Value**: ₹{pipeline_sum['pipeline_value_inr']:,.2f}
- **Total Prospects in Pipeline**: {pipeline_sum['total_leads']} (Won Deals: {pipeline_sum['won_count']})

---

### 🏛️ 2. Autonomous Commerce Portfolio
- **Active Business Units**: {commerce['total_business_units']} / 10
- **Portfolio Gross Margin**: {commerce['average_gross_margin_pct']}%
- **High-Margin Units (≥85%)**: {commerce['high_margin_units_count']}

---

### 📊 3. Multi-Market Snapshot
| Symbol | Class | Price | 24h Change |
|---|---|---|---|
{quotes_table}

---

### 🛡️ 4. Systems, Storage & 24/7 Operations
- **Database Status**: {diagnostics['database_status']}
- **Disk Storage Available**: {diagnostics['disk_available_gb']} GB
- **Process Memory RSS**: {diagnostics['memory_usage_mb']} MB
- **Overall Operating Status**: {diagnostics['overall_status']}

---

### 🎯 5. Top Strategic Priorities for Today
1. Prioritize outreach to high-conversion SMB prospects in {settings.primary_market}.
2. Review automated WhatsApp catalogue inquiries.
3. Validate Aether geospatial flood thresholds ahead of monsoon shifts.
"""
        file_path.write_text(content, encoding="utf-8")
        return file_path
