from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
from omniverse.modules.saas_factory.scaffolder import SaaSFactoryScaffolder

class ScaffoldRequest(BaseModel):
    name: str
    target_dir: str = "./generated_saas"
    include_auth: bool = True
    pricing_model: str = "freemium"

def get_saas_router():
    router = APIRouter(prefix="/saas", tags=["SaaS Factory"])

    @router.post("/scaffold")
    def scaffold_saas(req: ScaffoldRequest):
        scaffolder = SaaSFactoryScaffolder()
        return scaffolder.scaffold_project(
            app_name=req.name,
            target_dir=Path(req.target_dir),
            include_auth=req.include_auth,
            pricing_model=req.pricing_model
        )

    return router
