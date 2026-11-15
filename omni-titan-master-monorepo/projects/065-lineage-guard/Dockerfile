FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_065_lineage_guard

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_065_lineage_guard /app/omni_065_lineage_guard
USER nonroot:nonroot
EXPOSE 9065
ENTRYPOINT ["/app/omni_065_lineage_guard"]
