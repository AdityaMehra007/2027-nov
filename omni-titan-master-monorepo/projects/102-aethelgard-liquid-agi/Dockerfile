FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_102_aethelgard_liquid_agi

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_102_aethelgard_liquid_agi /app/omni_102_aethelgard_liquid_agi
USER nonroot:nonroot
EXPOSE 9102
ENTRYPOINT ["/app/omni_102_aethelgard_liquid_agi"]
