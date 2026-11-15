FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_107_biogenesis_rna_crispr

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_107_biogenesis_rna_crispr /app/omni_107_biogenesis_rna_crispr
USER nonroot:nonroot
EXPOSE 9107
ENTRYPOINT ["/app/omni_107_biogenesis_rna_crispr"]
