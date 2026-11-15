FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_026_quant_swarm

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_026_quant_swarm /app/omni_026_quant_swarm
USER nonroot:nonroot
EXPOSE 9026
ENTRYPOINT ["/app/omni_026_quant_swarm"]
