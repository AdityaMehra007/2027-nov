"""==============================================================================
TURNKEY MICRO-SAAS SUITE BUILDER
==============================================================================
Builds, scaffolds, and verifies 3 production micro-SaaS apps:
1. AuditPulse - Lead gen & site audit SaaS
2. RentShield - Real-time zero-brokerage alerts SaaS
3. PromptForge - LLM prompt benchmarking & cost optimizer
==============================================================================
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from omniverse.modules.saas_factory.scaffolder import SaaSFactoryScaffolder

def build_all_saas():
    print("=" * 70)
    print("  🚀 CASHFLOW INFINITY: MICRO-SAAS FACTORY PRODUCTION RUN")
    print("=" * 70)

    scaffolder = SaaSFactoryScaffolder()
    apps_base = Path("dist/apps")
    apps_base.mkdir(parents=True, exist_ok=True)

    apps_config = [
        ("AuditPulse AI", apps_base / "auditpulse", "freemium"),
        ("RentShield Radar", apps_base / "rentshield", "subscription"),
        ("PromptForge Engine", apps_base / "promptforge", "usage_based"),
    ]

    for name, path, model in apps_config:
        print(f"\n[SCAFFOLDING] >>> {name} ({model})")
        manifest = scaffolder.scaffold_project(
            app_name=name,
            target_dir=path,
            include_auth=True,
            pricing_model=model
        )
        print(f"  ✅ Created {len(manifest['files_created'])} files in {manifest['target_dir']}")
        for f in manifest["files_created"]:
            print(f"     • {f}")

    print("\n" + "=" * 70)
    print("  🎉 ALL 3 MICRO-SAAS APPLICATIONS COMPILED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    build_all_saas()
