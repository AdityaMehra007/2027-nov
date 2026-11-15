FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_021_omega_book

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_021_omega_book /app/omni_021_omega_book
USER nonroot:nonroot
EXPOSE 9021
ENTRYPOINT ["/app/omni_021_omega_book"]
