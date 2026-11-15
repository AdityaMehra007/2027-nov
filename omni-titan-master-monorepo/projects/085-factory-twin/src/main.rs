mod engine;
use axum::{extract::State, http::StatusCode, response::IntoResponse, routing::{get, post}, Json, Router};
use engine::{DomainEngine, DomainInput};
use std::{net::SocketAddr, sync::Arc};

async fn exec_h(State(eng): State<Arc<DomainEngine>>, Json(inp): Json<DomainInput>) -> impl IntoResponse {
    (StatusCode::CREATED, Json(eng.execute(inp)))
}

async fn health_h() -> impl IntoResponse {
    Json(serde_json::json!({ "project_id": 85, "slug": "factory-twin", "algorithm": "Discrete Fourier Transform Bearing Vibration Analyzer", "status": "ONLINE" }))
}

#[tokio::main]
async fn main() {
    let eng = Arc::new(DomainEngine::new());
    let app = Router::new()
        .route("/api/v1/execute", post(exec_h))
        .route("/healthz", get(health_h))
        .with_state(eng);
    let addr = SocketAddr::from(([0, 0, 0, 0], 9085));
    if let Ok(l) = tokio::net::TcpListener::bind(addr).await {
        let _ = axum::serve(l, app).await;
    }
}
