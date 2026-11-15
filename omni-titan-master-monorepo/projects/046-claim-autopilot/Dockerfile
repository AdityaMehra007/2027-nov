FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_046_claim_autopilot

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_046_claim_autopilot /app/omni_046_claim_autopilot
USER nonroot:nonroot
EXPOSE 9046
ENTRYPOINT ["/app/omni_046_claim_autopilot"]
