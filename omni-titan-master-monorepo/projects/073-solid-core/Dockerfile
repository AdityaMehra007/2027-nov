FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_073_solid_core

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_073_solid_core /app/omni_073_solid_core
USER nonroot:nonroot
EXPOSE 9073
ENTRYPOINT ["/app/omni_073_solid_core"]
