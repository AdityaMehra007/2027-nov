FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_048_bio_twin

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_048_bio_twin /app/omni_048_bio_twin
USER nonroot:nonroot
EXPOSE 9048
ENTRYPOINT ["/app/omni_048_bio_twin"]
