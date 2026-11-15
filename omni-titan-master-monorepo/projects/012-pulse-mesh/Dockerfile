FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_012_pulse_mesh

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_012_pulse_mesh /app/omni_012_pulse_mesh
USER nonroot:nonroot
EXPOSE 9012
ENTRYPOINT ["/app/omni_012_pulse_mesh"]
