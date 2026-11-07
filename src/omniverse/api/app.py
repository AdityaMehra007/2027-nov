from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from omniverse.core.config import OmniverseSettings, get_settings
from omniverse.core.database import DatabaseEngine, get_engine
from omniverse.api.routes.dashboard import get_dashboard_router
from omniverse.api.routes.revenue import get_revenue_router
from omniverse.api.routes.intel import get_intel_router
from omniverse.api.routes.ops import get_ops_router
from omniverse.api.routes.aether import get_aether_router
from omniverse.api.routes.saas import get_saas_router
from omniverse.api.routes.ws import get_ws_router
from omniverse.api.routes.planetary import get_planetary_router
from omniverse.api.routes.bangalore import get_bangalore_router
from omniverse.api.routes.agency import get_agency_router
from omniverse.api.routes.webhooks import get_webhooks_router
from omniverse.api.routes.portal import get_portal_router
from omniverse.api.routes.clearing import get_clearing_router
from omniverse.api.routes.finance import get_finance_router
from omniverse.ui.aether_map import render_aether_map_html
from omniverse.ui.cockpit_template import render_conglomerate_cockpit_html
from omniverse.ui.saas_portal_template import render_saas_portal_html
from omniverse.ui.mesh_monitor_template import render_mesh_monitor_html

def create_app(
    db_engine: DatabaseEngine | None = None,
    settings: OmniverseSettings | None = None,
) -> FastAPI:
    engine = db_engine or get_engine()
    engine.init_db()

    app_settings = settings or get_settings()
    is_production = bool(app_settings.env and str(app_settings.env).strip().lower() == "production")

    docs_url = None if is_production else "/docs"
    redoc_url = None if is_production else "/redoc"
    openapi_url = None if is_production else "/openapi.json"

    app = FastAPI(
        title="CASHFLOW INFINITY: OMNIVERSE Command Center API",
        version="1.0.0",
        description="Autonomous Revenue, Market Intelligence, and Operations Engine API",
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
    )

    raw_allowed_hosts = getattr(app_settings, "allowed_hosts", None) or ["127.0.0.1", "localhost", "testserver", "*"]
    if isinstance(raw_allowed_hosts, str):
        allowed_hosts = [h.strip() for h in raw_allowed_hosts.split(",") if h.strip()]
    else:
        allowed_hosts = list(raw_allowed_hosts)
    if "testserver" not in allowed_hosts and "*" not in allowed_hosts:
        allowed_hosts.append("testserver")
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts,
    )

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "connect-src 'self' ws: wss:; "
            "script-src 'self' 'unsafe-inline';"
        )
        return response

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
    app.include_router(get_bangalore_router(get_session), prefix="/api/v1")
    app.include_router(get_agency_router(), prefix="/api/v1")
    app.include_router(get_webhooks_router(get_session), prefix="/api/v1")
    app.include_router(get_clearing_router(), prefix="/api/v1")
    app.include_router(get_finance_router(), prefix="/api/v1")
    app.include_router(get_portal_router(get_session))

    @app.get("/")
    def root():
        return {
            "system": "CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC",
            "status": "OPERATIONAL",
            "docs": docs_url,
            "dashboard": "/dashboard"
        }

    @app.get("/dashboard", include_in_schema=False)
    @app.get("/dashboard/", include_in_schema=False)
    def dashboard_redirect():
        return RedirectResponse(url="/api/v1/dashboard/")

    @app.get("/aether-map", include_in_schema=False, response_class=HTMLResponse)
    def aether_map_root():
        return HTMLResponse(content=render_aether_map_html())

    @app.get("/cockpit", include_in_schema=False, response_class=HTMLResponse)
    def conglomerate_cockpit_root():
        return HTMLResponse(content=render_conglomerate_cockpit_html())

    @app.get("/saas", include_in_schema=False, response_class=HTMLResponse)
    def saas_portal_root():
        return HTMLResponse(content=render_saas_portal_html())

    @app.get("/mesh-monitor", include_in_schema=False, response_class=HTMLResponse)
    def mesh_monitor_root():
        return HTMLResponse(content=render_mesh_monitor_html())

    return app
