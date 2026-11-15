FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_051_nexus_erp

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_051_nexus_erp /app/omni_051_nexus_erp
USER nonroot:nonroot
EXPOSE 9051
ENTRYPOINT ["/app/omni_051_nexus_erp"]
