FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_087_warehouse_flow

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_087_warehouse_flow /app/omni_087_warehouse_flow
USER nonroot:nonroot
EXPOSE 9087
ENTRYPOINT ["/app/omni_087_warehouse_flow"]
