FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_105_citadel_omega_mm

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_105_citadel_omega_mm /app/omni_105_citadel_omega_mm
USER nonroot:nonroot
EXPOSE 9105
ENTRYPOINT ["/app/omni_105_citadel_omega_mm"]
