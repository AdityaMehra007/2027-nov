FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_083_chain_pulse

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_083_chain_pulse /app/omni_083_chain_pulse
USER nonroot:nonroot
EXPOSE 9083
ENTRYPOINT ["/app/omni_083_chain_pulse"]
