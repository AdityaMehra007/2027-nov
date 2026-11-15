FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_057_procure_mind

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_057_procure_mind /app/omni_057_procure_mind
USER nonroot:nonroot
EXPOSE 9057
ENTRYPOINT ["/app/omni_057_procure_mind"]
