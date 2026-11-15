FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_044_genome_stream

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_044_genome_stream /app/omni_044_genome_stream
USER nonroot:nonroot
EXPOSE 9044
ENTRYPOINT ["/app/omni_044_genome_stream"]
