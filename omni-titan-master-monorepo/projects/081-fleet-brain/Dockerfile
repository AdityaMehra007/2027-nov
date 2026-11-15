FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_081_fleet_brain

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_081_fleet_brain /app/omni_081_fleet_brain
USER nonroot:nonroot
EXPOSE 9081
ENTRYPOINT ["/app/omni_081_fleet_brain"]
