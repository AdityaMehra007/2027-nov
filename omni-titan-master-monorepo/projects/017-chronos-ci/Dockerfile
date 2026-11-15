FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_017_chronos_ci

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_017_chronos_ci /app/omni_017_chronos_ci
USER nonroot:nonroot
EXPOSE 9017
ENTRYPOINT ["/app/omni_017_chronos_ci"]
