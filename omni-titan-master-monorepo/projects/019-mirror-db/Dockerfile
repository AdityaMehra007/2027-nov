FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_019_mirror_db

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_019_mirror_db /app/omni_019_mirror_db
USER nonroot:nonroot
EXPOSE 9019
ENTRYPOINT ["/app/omni_019_mirror_db"]
