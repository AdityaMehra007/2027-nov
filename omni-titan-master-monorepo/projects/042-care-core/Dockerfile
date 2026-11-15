FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_042_care_core

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_042_care_core /app/omni_042_care_core
USER nonroot:nonroot
EXPOSE 9042
ENTRYPOINT ["/app/omni_042_care_core"]
