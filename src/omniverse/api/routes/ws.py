from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlmodel import Session
from omniverse.core.database import get_engine
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.operations.health import HealthDiagnostics
from omniverse.core.telemetry import global_event_bus
import asyncio

def get_ws_router():
    router = APIRouter(prefix="/ws", tags=["WebSockets"])

    @router.websocket("/telemetry")
    async def websocket_telemetry_endpoint(websocket: WebSocket):
        await websocket.accept()
        engine = get_engine()

        # Send initial snapshot
        try:
            with engine.get_session() as session:
                pipeline = LeadPipeline(session)
                payments = PaymentWorkflow(session)
                diagnostics = HealthDiagnostics(session)

                initial_payload = {
                    "type": "INITIAL_STATE",
                    "pipeline_summary": pipeline.get_pipeline_summary(),
                    "financial_ledger": payments.get_financial_ledger(),
                    "health": diagnostics.run_diagnostics(),
                    "recent_events": global_event_bus.get_events(limit=10)
                }
                await websocket.send_json(initial_payload)

            # Listen for client pings or heartbeats
            while True:
                data = await websocket.receive_text()
                if data == "ping":
                    await websocket.send_json({"type": "PONG"})
                elif data == "poll":
                    with engine.get_session() as session:
                        ledger = PaymentWorkflow(session).get_financial_ledger()
                        pipe = LeadPipeline(session).get_pipeline_summary()
                        await websocket.send_json({
                            "type": "SNAPSHOT",
                            "financial_ledger": ledger,
                            "pipeline_summary": pipe
                        })
        except WebSocketDisconnect:
            pass

    return router
