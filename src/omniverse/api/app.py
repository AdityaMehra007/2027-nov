from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from omniverse.core.database import DatabaseEngine, get_engine
from omniverse.api.routes.dashboard import get_dashboard_router
from omniverse.api.routes.revenue import get_revenue_router
from omniverse.api.routes.intel import get_intel_router
from omniverse.api.routes.ops import get_ops_router
from omniverse.api.routes.aether import get_aether_router
from omniverse.api.routes.saas import get_saas_router
from omniverse.api.routes.ws import get_ws_router
from omniverse.api.routes.planetary import get_planetary_router

def create_app(db_engine: DatabaseEngine | None = None) -> FastAPI:
    engine = db_engine or get_engine()
    engine.init_db()

    app = FastAPI(
        title="CASHFLOW INFINITY: OMNIVERSE Command Center API",
        version="1.0.0",
        description="Autonomous Revenue, Market Intelligence, and Operations Engine API"
    )

    def get_session():
        with engine.get_session() as session:
            yield session

    # Include routers under /api/v1
    app.include_router(get_dashboard_router(get_session), prefix="/api/v1")
    app.include_router(get_revenue_router(get_session), prefix="/api/v1")
    app.include_router(get_intel_router(), prefix="/api/v1")
    app.include_router(get_ops_router(get_session), prefix="/api/v1")
    app.include_router(get_aether_router(), prefix="/api/v1")
    app.include_router(get_saas_router(), prefix="/api/v1")
    app.include_router(get_ws_router(), prefix="/api/v1")
    app.include_router(get_planetary_router(), prefix="/api/v1")

    @app.get("/")
    def root():
        return {
            "system": "CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC",
            "status": "OPERATIONAL",
            "docs": "/docs",
            "dashboard": "/dashboard"
        }

    @app.get("/dashboard", include_in_schema=False)
    @app.get("/dashboard/", include_in_schema=False)
    def dashboard_redirect():
        return RedirectResponse(url="/api/v1/dashboard/")

    return app
