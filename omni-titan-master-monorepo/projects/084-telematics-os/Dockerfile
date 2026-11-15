FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_084_telematics_os

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_084_telematics_os /app/omni_084_telematics_os
USER nonroot:nonroot
EXPOSE 9084
ENTRYPOINT ["/app/omni_084_telematics_os"]
