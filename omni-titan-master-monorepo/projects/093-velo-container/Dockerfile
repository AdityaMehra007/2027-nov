FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_093_velo_container

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_093_velo_container /app/omni_093_velo_container
USER nonroot:nonroot
EXPOSE 9093
ENTRYPOINT ["/app/omni_093_velo_container"]
