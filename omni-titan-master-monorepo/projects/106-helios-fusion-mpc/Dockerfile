FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_106_helios_fusion_mpc

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_106_helios_fusion_mpc /app/omni_106_helios_fusion_mpc
USER nonroot:nonroot
EXPOSE 9106
ENTRYPOINT ["/app/omni_106_helios_fusion_mpc"]
