FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_112_sovereign_cashflow_engine

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_112_sovereign_cashflow_engine /app/omni_112_sovereign_cashflow_engine
USER nonroot:nonroot
EXPOSE 9112
ENTRYPOINT ["/app/omni_112_sovereign_cashflow_engine"]
