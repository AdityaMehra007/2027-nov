from fastapi import FastAPI
from omniverse.core.database import DatabaseEngine, get_engine
from omniverse.api.routes.dashboard import get_dashboard_router
from omniverse.api.routes.revenue import get_revenue_router
from omniverse.api.routes.intel import get_intel_router
from omniverse.api.routes.ops import get_ops_router

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

    @app.get("/")
    def root():
        return {
            "system": "CASHFLOW INFINITY: OMNIVERSE",
            "status": "OPERATIONAL",
            "docs": "/docs"
        }

    return app
