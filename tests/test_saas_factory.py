import pytest
from omniverse.modules.saas_factory.scaffolder import SaaSFactoryScaffolder

def test_saas_factory_scaffolding(tmp_path):
    scaffolder = SaaSFactoryScaffolder()
    output_dir = tmp_path / "micro_saas_app"
    
    manifest = scaffolder.scaffold_project(
        app_name="DocuMind AI",
        target_dir=output_dir,
        include_auth=True,
        pricing_model="freemium"
    )
    
    assert manifest["app_name"] == "DocuMind AI"
    assert (output_dir / "main.py").exists()
    assert (output_dir / "requirements.txt").exists()
    assert (output_dir / "README.md").exists()
    
    content = (output_dir / "main.py").read_text(encoding="utf-8")
    assert "DocuMind AI" in content
    assert "FastAPI" in content
