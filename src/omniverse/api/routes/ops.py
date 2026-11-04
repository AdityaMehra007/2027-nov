from fastapi import APIRouter, Depends
from sqlmodel import Session
from omniverse.operations.health import HealthDiagnostics

def get_ops_router(get_session_dep):
    router = APIRouter(prefix="/ops", tags=["Operations"])

    @router.get("/health")
    def get_health(session: Session = Depends(get_session_dep)):
        diagnostics = HealthDiagnostics(session)
        return diagnostics.run_diagnostics()

    return router
