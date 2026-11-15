FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_089_carbon_ledger

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_089_carbon_ledger /app/omni_089_carbon_ledger
USER nonroot:nonroot
EXPOSE 9089
ENTRYPOINT ["/app/omni_089_carbon_ledger"]
