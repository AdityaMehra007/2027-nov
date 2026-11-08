import warnings
import pytest
from starlette.exceptions import StarletteDeprecationWarning

warnings.filterwarnings("ignore", category=StarletteDeprecationWarning)

from fastapi.testclient import TestClient
from omniverse.api.app import app
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


def test_saas_factory_path_traversal_rejected(tmp_path):
    scaffolder = SaaSFactoryScaffolder(sandbox_root=tmp_path / "sandbox")
    with pytest.raises(ValueError, match="Path traversal detected"):
        scaffolder.scaffold_project(
            app_name="Malicious App",
            target_dir=tmp_path / "outside",
            include_auth=True,
            pricing_model="freemium"
        )


def test_saas_factory_dotdot_traversal_rejected():
    scaffolder = SaaSFactoryScaffolder()
    with pytest.raises(ValueError, match="Path traversal detected"):
        scaffolder.scaffold_project(
            app_name="Malicious App",
            target_dir="../../outside_sandbox",
            include_auth=True,
            pricing_model="freemium"
        )


def test_saas_factory_relative_leading_slash_rejected():
    scaffolder = SaaSFactoryScaffolder()
    with pytest.raises(ValueError, match="Path traversal detected"):
        scaffolder.scaffold_project(
            app_name="Malicious App",
            target_dir="/leading/slash/path",
            include_auth=True,
            pricing_model="freemium"
        )


def test_saas_scaffold_route_path_traversal_rejected():
    client = TestClient(app)
    res = client.post(
        "/api/v1/saas/scaffold",
        json={
            "name": "Malicious App",
            "target_dir": "../../../../../etc/passwd",
            "include_auth": True,
            "pricing_model": "freemium"
        }
    )
    assert res.status_code == 400
    assert "Path traversal detected" in res.json()["detail"]
