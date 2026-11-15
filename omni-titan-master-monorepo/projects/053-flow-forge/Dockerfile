FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_053_flow_forge

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_053_flow_forge /app/omni_053_flow_forge
USER nonroot:nonroot
EXPOSE 9053
ENTRYPOINT ["/app/omni_053_flow_forge"]
