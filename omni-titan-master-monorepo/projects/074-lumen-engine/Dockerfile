FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_074_lumen_engine

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_074_lumen_engine /app/omni_074_lumen_engine
USER nonroot:nonroot
EXPOSE 9074
ENTRYPOINT ["/app/omni_074_lumen_engine"]
